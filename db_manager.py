import os
import logging
import psycopg2
from psycopg2 import pool
from flask import g
from config import Config

logger = logging.getLogger(__name__)

_pool = None

def init_pool():
    global _pool
    _pool = pool.ThreadedConnectionPool(
        minconn=2,
        maxconn=int(os.environ.get('DB_POOL_MAX', 10)),
        dsn=Config.DATABASE_URL,
        options="-c statement_timeout=30000"
    )

def get_pool():
    global _pool
    if _pool is None or _pool.closed:
        init_pool()
    return _pool


class Row:
    """Attribute access (case-insensitive) + index access on DB rows."""
    def __init__(self, description, data):
        self._keys = [d[0] for d in description]
        self._data = list(data)
        self._lookup = {k.lower(): v for k, v in zip(self._keys, self._data)}

    def __getattr__(self, name):
        try:
            return self._lookup[name.lower()]
        except KeyError:
            raise AttributeError(f"Row has no column '{name}'")

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._data[key]
        return self._lookup[key.lower()]

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return f"Row({dict(zip(self._keys, self._data))})"


class WrappedCursor:
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query, params=None):
        self._cursor.execute(query, params)
        return self

    def fetchone(self):
        row = self._cursor.fetchone()
        if row is None:
            return None
        return Row(self._cursor.description, row)

    def fetchall(self):
        rows = self._cursor.fetchall()
        if not rows:
            return []
        desc = self._cursor.description
        return [Row(desc, row) for row in rows]

    def __getattr__(self, name):
        return getattr(self._cursor, name)


class WrappedConnection:
    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        return WrappedCursor(self._conn.cursor())

    def __getattr__(self, name):
        return getattr(self._conn, name)


def get_db_connection():
    """
    Her HTTP isteğinde Flask'ın g nesnesine bağlantı bağlar.
    Aynı istek içinde tekrar çağrılırsa aynı bağlantıyı döndürür.
    İstek bitince close_db() otomatik olarak bağlantıyı havuza iade eder.
    """
    if 'db' not in g:
        p = get_pool()
        raw_conn = p.getconn()
        # Bağlantı sağlık kontrolü – ölü bağlantıları tespit et
        try:
            raw_conn.cursor().execute("SELECT 1")
        except Exception:
            p.putconn(raw_conn, close=True)
            raw_conn = p.getconn()
        g.db = WrappedConnection(raw_conn)
    return g.db


def close_db(error=None):
    """app.teardown_appcontext ile kayıt edilir — route'larda conn.close() gerekmez."""
    wrapped = g.pop('db', None)
    if wrapped is not None:
        try:
            if error:
                wrapped._conn.rollback()
            get_pool().putconn(wrapped._conn)
        except Exception as e:
            logger.warning(f"Bağlantı havuza iade edilirken hata: {e}")