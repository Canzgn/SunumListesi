"""
Storage Service – Sunum dosyaları için backend bağımsız soyutlama (SOLID/DIP).

İki backend desteklenir:
- LocalBackend     : static/uploads/sunumlar/ altına kaydeder (development / fallback)
- SupabaseBackend  : Supabase Storage REST API üzerinden çalışır (production)

Hangi backend'in kullanılacağı SUPABASE_URL + SUPABASE_KEY varlığına göre
otomatik seçilir. Hiç biri ayarlanmazsa local'a düşer.
"""

import os
import uuid
import logging
from typing import Optional, BinaryIO

from flask import current_app

logger = logging.getLogger(__name__)


class StorageError(Exception):
    """Storage işlemleri için ortak istisna."""


# --------------------------------------------------------------------------
# Backend'ler
# --------------------------------------------------------------------------

class _LocalBackend:
    """Dosyaları yerel diskte (static/uploads/sunumlar) saklayan backend."""

    is_remote = False

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def upload(self, file_stream: BinaryIO, key: str) -> int:
        full_path = os.path.join(self.base_dir, key)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        size = 0
        with open(full_path, 'wb') as f:
            while True:
                chunk = file_stream.read(8192)
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)
        return size

    def delete(self, key: str) -> None:
        full_path = os.path.join(self.base_dir, key)
        try:
            if os.path.isfile(full_path):
                os.remove(full_path)
        except OSError as e:
            logger.warning("Yerel dosya silinemedi (%s): %s", key, e)

    def open_for_send(self, key: str):
        """(directory, filename) – Flask send_from_directory için."""
        full_path = os.path.join(self.base_dir, key)
        if not os.path.isfile(full_path):
            raise StorageError(f"Dosya bulunamadı: {key}")
        return os.path.dirname(full_path), os.path.basename(full_path)

    def get_signed_url(self, key: str, expires_in: int = 900) -> Optional[str]:
        return None  # Local'da Flask download route'u kullanılır.


class _SupabaseBackend:
    """Supabase Storage REST API backend'i (özel/private bucket için)."""

    is_remote = True

    def __init__(self, url: str, key: str, bucket: str):
        self.url = url.rstrip('/')
        self.key = key
        self.bucket = bucket
        self._headers = {
            'Authorization': f'Bearer {key}',
            'apikey': key,
        }

    def upload(self, file_stream: BinaryIO, key: str) -> int:
        import requests
        data = file_stream.read()
        size = len(data)
        endpoint = f"{self.url}/storage/v1/object/{self.bucket}/{key}"
        r = requests.post(
            endpoint,
            data=data,
            headers={**self._headers,
                     'Content-Type': 'application/octet-stream',
                     'x-upsert': 'true'},
            timeout=60
        )
        if r.status_code >= 300:
            raise StorageError(f"Supabase upload başarısız ({r.status_code}): {r.text[:200]}")
        return size

    def delete(self, key: str) -> None:
        import requests
        endpoint = f"{self.url}/storage/v1/object/{self.bucket}"
        r = requests.delete(
            endpoint,
            json={'prefixes': [key]},
            headers={**self._headers, 'Content-Type': 'application/json'},
            timeout=30
        )
        if r.status_code >= 300:
            logger.warning("Supabase silme uyarısı (%s): %s", r.status_code, r.text[:200])

    def get_signed_url(self, key: str, expires_in: int = 900) -> Optional[str]:
        import requests
        endpoint = f"{self.url}/storage/v1/object/sign/{self.bucket}/{key}"
        r = requests.post(
            endpoint,
            json={'expiresIn': expires_in},
            headers={**self._headers, 'Content-Type': 'application/json'},
            timeout=10
        )
        if r.status_code >= 300:
            raise StorageError(f"Signed URL üretilemedi ({r.status_code}): {r.text[:200]}")
        body = r.json()
        signed = body.get('signedURL') or body.get('signedUrl')
        if signed and signed.startswith('/'):
            return f"{self.url}/storage/v1{signed}"
        return signed

    def open_for_send(self, key: str):
        raise StorageError("Supabase backend'inde open_for_send yok; signed URL kullanın.")


# --------------------------------------------------------------------------
# Factory & helpers
# --------------------------------------------------------------------------

_backend = None


def get_storage():
    """Aktif backend'i döner (lazy init, process-wide singleton)."""
    global _backend
    if _backend is not None:
        return _backend

    cfg = current_app.config
    url = cfg.get('SUPABASE_URL')
    key = cfg.get('SUPABASE_KEY')
    bucket = cfg.get('SUPABASE_BUCKET', 'sunumlar')

    if url and key:
        _backend = _SupabaseBackend(url, key, bucket)
        logger.info("Storage backend: Supabase (bucket=%s)", bucket)
    else:
        # /<repo>/static/uploads/sunumlar
        base = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'static', 'uploads', 'sunumlar'
        )
        _backend = _LocalBackend(base)
        logger.info("Storage backend: Local (%s)", base)
    return _backend


def reset_storage():
    """Test ve config değişikliği durumları için backend'i sıfırlar."""
    global _backend
    _backend = None


def build_object_key(sunum_id: int, dosya_tipi: str, original_filename: str) -> str:
    """Bucket içindeki kararlı, çakışmasız dosya yolunu üretir."""
    from werkzeug.utils import secure_filename
    safe = secure_filename(original_filename) or 'dosya'
    return f"{sunum_id}/{dosya_tipi}_{uuid.uuid4().hex[:12]}_{safe}"
