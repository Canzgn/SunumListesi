import os
import sys
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32).hex())
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() in ('true', '1', 'yes')

    # Supabase / PostgreSQL bağlantı URL'si
    DATABASE_URL = os.environ.get('DATABASE_URL', '')

    # Session
    PERMANENT_SESSION_LIFETIME_HOURS = int(os.environ.get('SESSION_LIFETIME_HOURS', 4))
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_DEBUG', 'false').lower() not in ('true', '1', 'yes')

    # Öğrenci e-posta alan adı
    STUDENT_EMAIL_DOMAIN = os.environ.get('STUDENT_EMAIL_DOMAIN', 'ogrenci.edu.tr')

    # Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME', '')
    MAIL_SUPPRESS_SEND = not bool(os.environ.get('MAIL_USERNAME'))

    # Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'kimlikler')

    @classmethod
    def validate(cls):
        """Kritik ayarların varlığını doğrula. Eksikse çalışmayı durdur."""
        errors = []
        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL ortam değişkeni ayarlanmamış.")
        if not os.environ.get('SECRET_KEY'):
            import warnings
            warnings.warn(
                "SECRET_KEY ortam değişkeni ayarlanmamış — geçici rastgele anahtar kullanılıyor. "
                "Production'da SECRET_KEY mutlaka ayarlanmalı.",
                stacklevel=2
            )
        if errors:
            for e in errors:
                print(f"CONFIG HATASI: {e}", file=sys.stderr)
            sys.exit(1)