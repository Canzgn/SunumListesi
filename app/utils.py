"""
Yardımcı fonksiyonlar – SRP: Her fonksiyon tek bir sorumluluğa sahip.
Bu modül route'lara bağımlı değildir (Dependency Inversion).
"""

from flask import session, current_app, flash
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from db_manager import get_db_connection
from app.extensions import mail


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def log_islem(eylem, sunum_id=None, konu_adi=None, detay=None):
    """İşlem logu kaydet – hata olursa sessizce geç."""
    try:
        yapa = (session.get('admin_id') or session.get('hoca_name') or
                session.get('kontrolcu_name') or session.get('student_no') or 'sistem')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO IslemLoglari (Eylem, SunumID, KonuAdi, YapaAdi, Detay) VALUES (%s,%s,%s,%s,%s)",
            (eylem, sunum_id, konu_adi, str(yapa), detay)
        )
        conn.commit()
    except Exception as e:
        current_app.logger.warning(f"Log kaydedilemedi: {e}")


def try_send_email(to_addr, subject, body):
    """E-posta gönder; MAIL_USERNAME ayarlanmamışsa veya hata oluşursa sessizce geç."""
    if not current_app.config.get('MAIL_USERNAME'):
        return
    try:
        msg = Message(subject, recipients=[to_addr], body=body)
        mail.send(msg)
    except Exception as e:
        current_app.logger.warning(f"E-posta gönderilemedi ({to_addr}): {e}")


def basvuru_acik_mi(bolum_id=None, donem_id=None):
    """Seçili dönem/bölüm için başvuru süresi doldu mu? True = açık, False = kapalı."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if bolum_id:
            cursor.execute("SELECT d.BasvuruBitis FROM Bolumler b JOIN Donemler d ON b.DonemID=d.DonemID WHERE b.BolumID=%s", (bolum_id,))
        elif donem_id:
            cursor.execute("SELECT BasvuruBitis FROM Donemler WHERE DonemID=%s", (donem_id,))
        else:
            cursor.execute("SELECT BasvuruBitis FROM Donemler WHERE Aktif=TRUE ORDER BY DonemID LIMIT 1")
        row = cursor.fetchone()
        if row and row[0]:
            return datetime.now() < row[0]
    except Exception:
        pass
    return True


def get_admin_bolum_ids():
    """
    Admin için yetkili BolumID listesini döndürür.
    - Hoca → None (tüm bölümler)
    - Admin, AdminBolumler'de kayıt yoksa → None (geriye uyumluluk)
    - Admin, kayıt varsa → yalnızca kayıtlı BolumID'ler
    """
    role = session.get('user_role')
    if role == 'hoca':
        return None
    if role != 'admin':
        return []
    admin_id = session.get('admin_id')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT BolumID FROM AdminBolumler WHERE AdminID = %s", (admin_id,))
        rows = cursor.fetchall()
        if not rows:
            return None
        return [r.BolumID for r in rows]
    except Exception:
        return None


def get_admin_allowed_turs():
    """
    Admin için görülebilir OgretimTuru listesini döndürür.
    """
    bolum_ids = get_admin_bolum_ids()
    if bolum_ids is None:
        return ['Örgün', 'Gece']
    if not bolum_ids:
        return []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT OgretimTuru FROM Bolumler WHERE BolumID = ANY(%s)",
            (bolum_ids,)
        )
        rows = cursor.fetchall()
        return [r.OgretimTuru for r in rows] or ['Örgün', 'Gece']
    except Exception:
        return ['Örgün', 'Gece']


def kontrolcu_zaman_kontrol(sunum_tarihi):
    """Kontrolcünün bu başvuruya dokunup dokunamayacağını kontrol eder.
    Returns (ok: bool, mesaj: str)
    """
    from datetime import time, timedelta
    if not sunum_tarihi:
        return True, ''
    now = datetime.now()
    if hasattr(sunum_tarihi, 'date'):
        sd = sunum_tarihi.date()
    else:
        sd = sunum_tarihi
    pazar = sd + timedelta(days=(6 - sd.weekday()))
    deadline = datetime.combine(pazar, time(12, 0))
    baslangic = datetime.combine(sd, time(0, 0))
    if now < baslangic:
        return False, f'Bu başvuruya sunum günü ({sd.strftime("%d.%m.%Y")}) gelmeden işlem yapamazsınız.'
    if now > deadline:
        return False, f'Bu başvurunun düzenleme süresi dolmuş ({pazar.strftime("%d.%m.%Y")} 12:00).'
    return True, ''


def change_password(table, id_column, id_value, old_pw, new_pw, new_pw2):
    """Ortak şifre değiştirme mantığı. Başarılı ise True, değilse False döner.
    Flash mesajlarını otomatik ayarlar."""
    # Güvenlik: Tablo/kolon adlarını sabit whitelist ile doğrula (SQL Injection önlemi)
    ALLOWED_TABLES = {
        ('Admins', 'AdminID'),
        ('Hocalar', 'HocaID'),
        ('Ogrenciler', 'OgrenciNo'),
        ('SoruKontrolculeri', 'KontrolcuID'),
    }
    if (table, id_column) not in ALLOWED_TABLES:
        flash('Geçersiz işlem.', 'error')
        return False

    conn = get_db_connection()
    cursor = conn.cursor()
    # psycopg2 identifier quoting ile güvenli SQL oluştur
    from psycopg2 import sql
    query_select = sql.SQL("SELECT Password FROM {} WHERE {}=%s").format(
        sql.Identifier(table), sql.Identifier(id_column)
    )
    cursor._cursor.execute(query_select, (id_value,))
    raw_row = cursor._cursor.fetchone()
    pw = raw_row[0] if raw_row else None
    if not pw or not check_password_hash(pw, old_pw):
        flash('Mevcut şifre hatalı.', 'error')
        return False
    if len(new_pw) < 6:
        flash('Yeni şifre en az 6 karakter olmalı.', 'error')
        return False
    if new_pw != new_pw2:
        flash('Yeni şifreler eşleşmiyor.', 'error')
        return False
    query_update = sql.SQL("UPDATE {} SET Password=%s WHERE {}=%s").format(
        sql.Identifier(table), sql.Identifier(id_column)
    )
    cursor._cursor.execute(query_update, (generate_password_hash(new_pw), id_value))
    conn.commit()
    flash('Şifreniz başarıyla güncellendi.', 'success')
    return True
