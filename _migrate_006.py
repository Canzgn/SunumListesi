import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ['PYTHONIOENCODING'] = 'utf-8'
from dotenv import load_dotenv
load_dotenv()

import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ.get('DATABASE_URL', '')
SQL_PATH = os.path.join(os.path.dirname(__file__), 'migrations', '006_otomatik_yerlesim_gecmisi.sql')

with open(SQL_PATH, 'r', encoding='utf-8') as f:
    sql = f.read()

conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.NamedTupleCursor)
cursor = conn.cursor()
cursor.execute(sql)
conn.commit()
conn.close()
print("Migration 006 uygulandi: otomatikyerlesimgecmisi tablosu hazir.")
