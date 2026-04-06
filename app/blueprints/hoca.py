"""
Hoca (Öğretmen) Blueprint – Öğretmen paneli, bölüm/dönem yönetimi,
konu yönetimi, hafta yönetimi, takvim (SRP).
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort, current_app
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import psycopg2.errors

from db_manager import get_db_connection
from app.decorators import hoca_required
from app.helpers import build_schedule_data

hoca_bp = Blueprint('hoca', __name__)


def _verify_bolum_ownership(cursor, bolum_id, hoca_id):
    """Hoca'nın bölüme erişim yetkisi olup olmadığını kontrol eder."""
    cursor.execute(
        "SELECT 1 FROM HocaBolumler WHERE BolumID = %s AND HocaID = %s",
        (bolum_id, hoca_id)
    )
    if not cursor.fetchone():
        abort(403)


# --- Profil ---

@hoca_bp.route('/profil')
@hoca_required
def hoca_profil():
    if session.get('user_role') != 'hoca':
        return redirect(url_for('auth.login'))
    hoca_id = session['hoca_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT HocaID, Username, AdSoyad FROM Hocalar WHERE HocaID=%s", (hoca_id,))
    hoca = cursor.fetchone()
    cursor.execute("""
        SELECT b.BolumAdi, b.OgretimTuru, d.DonemAdi
        FROM HocaBolumler hb
        JOIN Bolumler b ON hb.BolumID = b.BolumID
        LEFT JOIN Donemler d ON b.DonemID = d.DonemID
        WHERE hb.HocaID = %s
        ORDER BY d.Aktif DESC, b.BolumAdi
    """, (hoca_id,))
    bolumler = cursor.fetchall()
    return render_template('hoca/hoca_profil.html', hoca=hoca, bolumler=bolumler)


# --- Yeni Öğretmen Ekle ---

@hoca_bp.route('/ogretmen_ekle', methods=['GET', 'POST'])
@hoca_required
def hoca_ogretmen_ekle():
    if session.get('user_role') != 'hoca':
        return redirect(url_for('auth.login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.BolumID, b.BolumAdi, b.OgretimTuru
        FROM HocaBolumler hb JOIN Bolumler b ON hb.BolumID = b.BolumID
        WHERE hb.HocaID = %s ORDER BY b.BolumAdi
    """, (session['hoca_id'],))
    bolumler = cursor.fetchall()

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        ad_soyad = request.form.get('ad_soyad', '').strip()
        bolum_ids = request.form.getlist('bolum_ids', type=int)
        if not username or not password:
            flash('Kullanıcı adı ve şifre zorunludur.', 'error')
            return render_template('hoca/hoca_ogretmen_ekle.html', bolumler=bolumler)
        cursor.execute("SELECT HocaID FROM Hocalar WHERE Username=%s", (username,))
        if cursor.fetchone():
            flash('Bu kullanıcı adı zaten kullanılıyor.', 'error')
            return render_template('hoca/hoca_ogretmen_ekle.html', bolumler=bolumler)
        pw_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO Hocalar (Username, Password, AdSoyad, IsApproved) VALUES (%s, %s, %s, TRUE) RETURNING HocaID",
            (username, pw_hash, ad_soyad or None)
        )
        new_id = cursor.fetchone()[0]
        for bid in bolum_ids:
            cursor.execute("INSERT INTO HocaBolumler (HocaID, BolumID) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                           (new_id, bid))
        conn.commit()
        flash(f'Öğretmen "{ad_soyad or username}" başarıyla eklendi ve otomatik onaylandı.')
        return redirect(url_for('hoca.hoca_ogretmen_ekle'))
    return render_template('hoca/hoca_ogretmen_ekle.html', bolumler=bolumler)


# --- Admin Bölüm Ata / Ad Güncelle (hoca yetkisi) ---

@hoca_bp.route('/admin_bolum_ata', methods=['POST'])
@hoca_required
def hoca_admin_bolum_ata():
    admin_id = request.form.get('admin_id', type=int)
    bolum_ids = request.form.getlist('bolum_ids', type=int)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM AdminBolumler WHERE AdminID = %s", (admin_id,))
    for bid in bolum_ids:
        cursor.execute("INSERT INTO AdminBolumler (AdminID, BolumID) VALUES (%s, %s) ON CONFLICT DO NOTHING", (admin_id, bid))
    conn.commit()
    flash("Admin bölüm yetkileri güncellendi.")
    return redirect(url_for('admin.manage_admins'))


@hoca_bp.route('/admin_adsoyad_guncelle', methods=['POST'])
@hoca_required
def hoca_admin_adsoyad():
    admin_id = request.form.get('admin_id', type=int)
    ad_soyad = request.form.get('ad_soyad', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Admins SET AdSoyad=%s WHERE AdminID=%s", (ad_soyad, admin_id))
    conn.commit()
    flash("Admin adı güncellendi.")
    return redirect(url_for('admin.manage_admins'))


# --- Panel ---

@hoca_bp.route('/panel')
@hoca_required
def hoca_panel():
    conn = get_db_connection()
    cursor = conn.cursor()

    hoca_id = session.get('hoca_id')
    cursor.execute("SELECT DonemID, DonemAdi, Aktif FROM Donemler ORDER BY Aktif DESC, DonemAdi DESC")
    donemler = cursor.fetchall()

    secili_donem_id = request.args.get('donem_id', '')
    if not secili_donem_id and donemler:
        for d in donemler:
            if d.Aktif:
                secili_donem_id = str(d.DonemID)
                break
        if not secili_donem_id:
            secili_donem_id = str(donemler[0].DonemID)

    if session['user_role'] == 'hoca':
        q = """
            SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi, d.DonemID
            FROM HocaBolumler hb
            JOIN Bolumler b ON hb.BolumID = b.BolumID
            JOIN Donemler d ON b.DonemID = d.DonemID
            WHERE hb.HocaID = %s
        """
        params = [hoca_id]
        if secili_donem_id:
            q += " AND d.DonemID = %s"
            params.append(secili_donem_id)
        q += " ORDER BY d.Aktif DESC, d.DonemAdi DESC, b.BolumAdi"
        cursor.execute(q, params)
    else:
        q = """
            SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi, d.DonemID
            FROM Bolumler b JOIN Donemler d ON b.DonemID = d.DonemID
        """
        params = []
        if secili_donem_id:
            q += " WHERE d.DonemID = %s"
            params.append(secili_donem_id)
        q += " ORDER BY d.Aktif DESC, d.DonemAdi DESC, b.BolumAdi"
        cursor.execute(q, params)
    bolumler = cursor.fetchall()

    # Tek sorguda tüm bölüm istatistiklerini al (N+1 query sorunu çözümü)
    bolum_ids = [b.BolumID for b in bolumler]
    stats_map = {}
    if bolum_ids:
        cursor.execute("""
            SELECT b.BolumID,
                   COUNT(DISTINCT o.OgrenciID) AS ogr_sayi,
                   COUNT(DISTINCT CASE WHEN o.IsApproved = TRUE THEN o.OgrenciID END) AS onaylanan_sayi,
                   COUNT(DISTINCT sp.SunumID) AS sunum_sayi,
                   COUNT(DISTINCT sg.GorevID) AS atanan_sayi
            FROM Bolumler b
            LEFT JOIN Ogrenciler o ON o.BolumID = b.BolumID
            LEFT JOIN SunumProgrami sp ON sp.BolumID = b.BolumID
            LEFT JOIN SunumGorevlileri sg ON sg.SunumID = sp.SunumID
            WHERE b.BolumID = ANY(%s)
            GROUP BY b.BolumID
        """, (bolum_ids,))
        for row in cursor.fetchall():
            stats_map[row.BolumID] = {
                'ogr_sayi': row.ogr_sayi,
                'onaylanan_sayi': row.onaylanan_sayi,
                'sunum_sayi': row.sunum_sayi,
                'atanan_sayi': row.atanan_sayi,
            }

    bolum_stats = []
    for b in bolumler:
        s = stats_map.get(b.BolumID, {'ogr_sayi': 0, 'onaylanan_sayi': 0, 'sunum_sayi': 0, 'atanan_sayi': 0})
        bolum_stats.append({
            'bolum': b, 'ogr_sayi': s['ogr_sayi'], 'onaylanan_sayi': s['onaylanan_sayi'],
            'sunum_sayi': s['sunum_sayi'], 'atanan_sayi': s['atanan_sayi']
        })

    return render_template('hoca/hoca_panel.html', bolum_stats=bolum_stats, donemler=donemler,
                           secili_donem_id=secili_donem_id)


# --- Sunum Panel ---

@hoca_bp.route('/sunum_panel')
@hoca_required
def hoca_sunum_panel():
    conn = get_db_connection()
    cursor = conn.cursor()

    if session['user_role'] == 'hoca':
        cursor.execute("""
            SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi, d.DonemID, d.Aktif
            FROM HocaBolumler hb
            JOIN Bolumler b ON hb.BolumID = b.BolumID
            JOIN Donemler d ON b.DonemID = d.DonemID
            WHERE hb.HocaID = %s
            ORDER BY d.Aktif DESC, d.DonemAdi DESC, b.BolumAdi
        """, (session['hoca_id'],))
    else:
        cursor.execute("""
            SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi, d.DonemID, d.Aktif
            FROM Bolumler b JOIN Donemler d ON b.DonemID = d.DonemID
            ORDER BY d.Aktif DESC, d.DonemAdi DESC, b.BolumAdi
        """)
    bolumler = cursor.fetchall()

    if not bolumler:
        return render_template('hoca/hoca_sunum_panel.html', schedule_data=[], bolumler=[],
                               secili_bolum=None, secili_bolum_id='')

    secili_bolum_id = request.args.get('bolum_id', '')
    if not secili_bolum_id:
        secili_bolum_id = str(bolumler[0].BolumID)
    secili_bolum_id = str(secili_bolum_id)
    secili_bolum = next((b for b in bolumler if str(b.BolumID) == secili_bolum_id), bolumler[0])

    cursor.execute("""
        SELECT sp.SunumID, sp.HaftaNo, k.KonuAdi, sp.OgretimTuru, sp.SunumTarihi
        FROM SunumProgrami sp
        JOIN Konular k ON k.KonuID = sp.KonuID
        WHERE sp.BolumID = %s OR (sp.BolumID IS NULL AND sp.OgretimTuru = %s)
        ORDER BY sp.HaftaNo, k.SiraNo
    """, (secili_bolum_id, secili_bolum.OgretimTuru))
    slots = cursor.fetchall()
    slot_ids = [s.SunumID for s in slots]

    if not slot_ids:
        return render_template('hoca/hoca_sunum_panel.html', schedule_data=[], bolumler=bolumler,
                               secili_bolum=secili_bolum, secili_bolum_id=secili_bolum_id)

    schedule_data = build_schedule_data(slot_ids, slots)

    return render_template('hoca/hoca_sunum_panel.html', schedule_data=schedule_data,
                           bolumler=bolumler, secili_bolum=secili_bolum,
                           secili_bolum_id=secili_bolum_id)


# --- Bölüm Ekle ---

@hoca_bp.route('/bolum_ekle', methods=['GET', 'POST'])
@hoca_required
def hoca_bolum_ekle():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        bolum_adi = request.form.get('bolum_adi', '').strip()
        ogretim_turu = request.form.get('ogretim_turu', 'Örgün')
        donem_id = request.form.get('donem_id')
        ogr_import = request.form.get('ogr_import', 'manual')

        try:
            cursor.execute("""
                INSERT INTO Bolumler (BolumAdi, OgretimTuru, DonemID)
                VALUES (%s, %s, %s) RETURNING BolumID
            """, (bolum_adi, ogretim_turu, donem_id))
            bolum_id = cursor.fetchone()[0]

            if session['user_role'] == 'hoca':
                cursor.execute("INSERT INTO HocaBolumler (HocaID, BolumID) VALUES (%s, %s)",
                               (session['hoca_id'], bolum_id))
            conn.commit()
            flash(f"'{bolum_adi}' bölümü oluşturuldu.")

            if ogr_import == 'excel':
                return redirect(url_for('hoca.hoca_ogrenci_import', bolum_id=bolum_id))
            elif ogr_import == 'manual':
                return redirect(url_for('hoca.hoca_ogrenci_listesi', bolum_id=bolum_id))
            else:
                return redirect(url_for('hoca.hoca_panel'))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            flash("Bu bölüm/tur/dönem kombinasyonu zaten mevcut!", "error")

    cursor.execute("SELECT DonemID, DonemAdi, Aktif FROM Donemler ORDER BY Aktif DESC, DonemAdi DESC")
    donemler = cursor.fetchall()
    return render_template('hoca/hoca_bolum_ekle.html', donemler=donemler)


# --- Dönem Ekle ---

@hoca_bp.route('/donem_ekle', methods=['POST'])
@hoca_required
def hoca_donem_ekle():
    donem_adi = request.form.get('donem_adi', '').strip()
    aktif = request.form.get('aktif') == 'on'
    redirect_to = request.form.get('redirect_to', 'hoca_panel')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if aktif:
            cursor.execute("UPDATE Donemler SET Aktif=FALSE")
        cursor.execute("INSERT INTO Donemler (DonemAdi, Aktif) VALUES (%s, %s)", (donem_adi, aktif))
        conn.commit()
        flash(f"'{donem_adi}' dönemi eklendi.")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        flash("Bu dönem zaten mevcut!", "error")
    if redirect_to == 'hoca_donemler':
        return redirect(url_for('hoca.hoca_donemler'))
    return redirect(url_for('hoca.hoca_panel'))


# --- Öğrenci Listesi & Ekleme & Import ---

@hoca_bp.route('/ogrenciler')
@hoca_required
def hoca_tum_ogrenciler():
    bolum_id = request.args.get('bolum_id')
    if bolum_id and bolum_id.isdigit():
        return redirect(url_for('hoca.hoca_ogrenci_listesi', bolum_id=int(bolum_id)))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    if session.get('user_role') == 'hoca':
        cursor.execute("""
            SELECT b.BolumID
            FROM HocaBolumler hb
            JOIN Bolumler b ON hb.BolumID = b.BolumID
            JOIN Donemler d ON b.DonemID = d.DonemID
            WHERE hb.HocaID = %s
            ORDER BY d.Aktif DESC, d.DonemAdi DESC, b.BolumAdi
            LIMIT 1
        """, (session['hoca_id'],))
    else:
        cursor.execute("""
            SELECT b.BolumID
            FROM Bolumler b JOIN Donemler d ON b.DonemID = d.DonemID
            ORDER BY d.Aktif DESC, d.DonemAdi DESC, b.BolumAdi
            LIMIT 1
        """)
    bolum = cursor.fetchone()
    if not bolum:
        flash("Henüz bir bölümünüz bulunmuyor.", "error")
        return redirect(url_for('hoca.hoca_panel'))
    return redirect(url_for('hoca.hoca_ogrenci_listesi', bolum_id=bolum.BolumID))


@hoca_bp.route('/bolum/<int:bolum_id>/ogrenciler')
@hoca_required
def hoca_ogrenci_listesi(bolum_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    _verify_bolum_ownership(cursor, bolum_id, session['hoca_id'])
    cursor.execute("""
        SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi
        FROM Bolumler b JOIN Donemler d ON b.DonemID=d.DonemID
        WHERE b.BolumID=%s
    """, (bolum_id,))
    bolum = cursor.fetchone()
    
    if session.get('user_role') == 'hoca':
        cursor.execute("""
            SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi, d.DonemID, d.Aktif
            FROM HocaBolumler hb
            JOIN Bolumler b ON hb.BolumID = b.BolumID
            JOIN Donemler d ON b.DonemID = d.DonemID
            WHERE hb.HocaID = %s
            ORDER BY d.Aktif DESC, d.DonemAdi DESC, b.BolumAdi
        """, (session['hoca_id'],))
    else:
        cursor.execute("""
            SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi, d.DonemID, d.Aktif
            FROM Bolumler b JOIN Donemler d ON b.DonemID = d.DonemID
            ORDER BY d.Aktif DESC, d.DonemAdi DESC, b.BolumAdi
        """)
    bolumler = cursor.fetchall()
    
    cursor.execute("""
        SELECT OgrenciID, OgrenciNo, AdSoyad, IsApproved, KayitTarihi
        FROM Ogrenciler WHERE BolumID=%s ORDER BY OgrenciNo
    """, (bolum_id,))
    ogrenciler = cursor.fetchall()
    return render_template('hoca/hoca_ogrenci_listesi.html', bolum=bolum, ogrenciler=ogrenciler, bolumler=bolumler, secili_bolum_id=str(bolum_id))


@hoca_bp.route('/bolum/<int:bolum_id>/ogrenci_ekle', methods=['POST'])
@hoca_required
def hoca_ogrenci_ekle(bolum_id):
    ogr_no = request.form.get('ogrenci_no', '').strip()
    ad_soyad = request.form.get('ad_soyad', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    _verify_bolum_ownership(cursor, bolum_id, session['hoca_id'])
    cursor.execute("SELECT OgretimTuru, DonemID FROM Bolumler WHERE BolumID=%s", (bolum_id,))
    b = cursor.fetchone()
    try:
        cursor.execute("""
            INSERT INTO Ogrenciler (OgrenciNo, AdSoyad, OgretimTuru, IsApproved, BolumID, DonemID)
            VALUES (%s, %s, %s, FALSE, %s, %s)
            ON CONFLICT (OgrenciNo) DO UPDATE
                SET AdSoyad=EXCLUDED.AdSoyad, BolumID=EXCLUDED.BolumID, DonemID=EXCLUDED.DonemID
        """, (ogr_no, ad_soyad, b.OgretimTuru, bolum_id, b.DonemID))
        conn.commit()
        flash(f"{ogr_no} eklendi.")
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Öğrenci ekleme hatası: {e}")
        flash("Öğrenci eklenirken bir hata oluştu.", "error")
    return redirect(url_for('hoca.hoca_ogrenci_listesi', bolum_id=bolum_id))


@hoca_bp.route('/bolum/<int:bolum_id>/import', methods=['GET', 'POST'])
@hoca_required
def hoca_ogrenci_import(bolum_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    _verify_bolum_ownership(cursor, bolum_id, session['hoca_id'])
    cursor.execute("""
        SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi, d.DonemID
        FROM Bolumler b JOIN Donemler d ON b.DonemID=d.DonemID WHERE b.BolumID=%s
    """, (bolum_id,))
    bolum = cursor.fetchone()

    if request.method == 'POST':
        file = request.files.get('excel_file')
        if not file or file.filename == '':
            flash("Dosya seçilmedi.", "error")
            return redirect(request.url)

        import openpyxl
        import io
        try:
            wb = openpyxl.load_workbook(io.BytesIO(file.read()))
            ws = wb.active
            added = 0
            for row in ws.iter_rows(values_only=True):
                if not row[0]:
                    continue
                val = str(row[0]).strip()
                try:
                    ogr_no = str(int(float(val)))
                except (ValueError, TypeError):
                    continue
                ad = str(row[1]).strip() if row[1] else ''
                cursor.execute("""
                    INSERT INTO Ogrenciler (OgrenciNo, AdSoyad, OgretimTuru, IsApproved, BolumID, DonemID)
                    VALUES (%s, %s, %s, FALSE, %s, %s)
                    ON CONFLICT (OgrenciNo) DO UPDATE
                        SET AdSoyad=COALESCE(NULLIF(EXCLUDED.AdSoyad,''), Ogrenciler.AdSoyad),
                            BolumID=EXCLUDED.BolumID, DonemID=EXCLUDED.DonemID
                """, (ogr_no, ad, bolum.OgretimTuru, bolum_id, bolum.DonemID))
                added += 1
            conn.commit()
            flash(f"{added} öğrenci içe aktarıldı.")
            return redirect(url_for('hoca.hoca_ogrenci_listesi', bolum_id=bolum_id))
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Import hatası: {e}")
            flash("İçe aktarma sırasında bir hata oluştu.", "error")

    return render_template('hoca/hoca_ogrenci_import.html', bolum=bolum)


# --- Kontrolcü Yönetimi ---

@hoca_bp.route('/kontrolcu_ekle', methods=['POST'])
@hoca_required
def hoca_kontrolcu_ekle():
    username = request.form.get('username', '').strip()
    ad_soyad = request.form.get('ad_soyad', '').strip()
    pw = request.form.get('password', '').strip()
    bolum_id = request.form.get('bolum_id') or None
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        hashed = generate_password_hash(pw)
        cursor.execute("""
            INSERT INTO SoruKontrolculeri (Username, Password, AdSoyad, IsApproved, BolumID)
            VALUES (%s, %s, %s, TRUE, %s)
        """, (username, hashed, ad_soyad, bolum_id))
        conn.commit()
        flash(f"'{username}' soru kontrolcüsü olarak eklendi.")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        flash("Bu kullanıcı adı zaten kayıtlı!", "error")
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Kontrolcü ekleme hatası: {e}")
        flash("Kontrolcü eklenirken bir hata oluştu.", "error")
    return redirect(url_for('hoca.hoca_kontrolcular'))


@hoca_bp.route('/kontrolcular')
@hoca_required
def hoca_kontrolcular():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sk.KontrolcuID, sk.Username, sk.AdSoyad, sk.IsApproved,
               b.BolumAdi, b.OgretimTuru, d.DonemAdi, b.BolumID
        FROM SoruKontrolculeri sk
        LEFT JOIN Bolumler b ON sk.BolumID=b.BolumID
        LEFT JOIN Donemler d ON b.DonemID=d.DonemID
        ORDER BY sk.AdSoyad
    """)
    kontrolcular = cursor.fetchall()

    if session['user_role'] == 'hoca':
        cursor.execute("""
            SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi
            FROM HocaBolumler hb
            JOIN Bolumler b ON hb.BolumID=b.BolumID
            JOIN Donemler d ON b.DonemID=d.DonemID
            WHERE hb.HocaID=%s ORDER BY d.Aktif DESC, b.BolumAdi
        """, (session['hoca_id'],))
    else:
        cursor.execute("""
            SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi
            FROM Bolumler b JOIN Donemler d ON b.DonemID=d.DonemID
            ORDER BY d.Aktif DESC, b.BolumAdi
        """)
    bolumler = cursor.fetchall()

    secili_bolum_id = request.args.get('bolum_id', '')
    bolum_ogrenciler = []
    if secili_bolum_id:
        cursor.execute("""
            SELECT OgrenciNo, AdSoyad FROM Ogrenciler
            WHERE BolumID=%s ORDER BY AdSoyad, OgrenciNo
        """, (secili_bolum_id,))
        bolum_ogrenciler = cursor.fetchall()

    return render_template('hoca/hoca_kontrolcular.html', kontrolcular=kontrolcular, bolumler=bolumler,
                           bolum_ogrenciler=bolum_ogrenciler, secili_bolum_id=secili_bolum_id)


@hoca_bp.route('/kontrolcu_sil/<int:k_id>', methods=['POST'])
@hoca_required
def hoca_kontrolcu_sil(k_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SoruKontrolculeri WHERE KontrolcuID=%s", (k_id,))
    conn.commit()
    flash("Soru kontrolcüsü silindi.")
    return redirect(url_for('hoca.hoca_kontrolcular'))


# --- Şifre Değiştirme ---

@hoca_bp.route('/sifre_degistir', methods=['POST'])
@hoca_required
def hoca_sifre_degistir():
    from app.utils import change_password
    change_password('Hocalar', 'HocaID', session['hoca_id'],
                    request.form.get('old_password', ''),
                    request.form.get('new_password', ''),
                    request.form.get('new_password2', ''))
    return redirect(url_for('hoca.hoca_panel'))


# --- Konu Yönetimi ---

@hoca_bp.route('/konular')
@hoca_required
def hoca_konular():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT KonuID, KonuAdi, SiraNo FROM Konular ORDER BY SiraNo, KonuAdi")
    konular = cursor.fetchall()
    cursor.execute("SELECT KonuID, COUNT(*) AS cnt FROM SunumProgrami GROUP BY KonuID")
    kullanim_map = {r.KonuID: r.cnt for r in cursor.fetchall()}
    return render_template('hoca/hoca_konular.html', konular=konular, kullanim_map=kullanim_map)


@hoca_bp.route('/konu_ekle', methods=['POST'])
@hoca_required
def hoca_konu_ekle():
    konu_adi = request.form.get('konu_adi', '').strip()
    sira_no = request.form.get('sira_no', '').strip()
    if not konu_adi:
        flash('Konu adı boş olamaz.', 'error')
        return redirect(url_for('hoca.hoca_konular'))
    try:
        sira_no = int(sira_no) if sira_no else 999
    except ValueError:
        sira_no = 999
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Konular (KonuAdi, SiraNo) VALUES (%s, %s)", (konu_adi, sira_no))
    conn.commit()
    flash(f"'{konu_adi}' konusu eklendi.")
    return redirect(url_for('hoca.hoca_konular'))


@hoca_bp.route('/konu_duzenle/<int:konu_id>', methods=['POST'])
@hoca_required
def hoca_konu_duzenle(konu_id):
    konu_adi = request.form.get('konu_adi', '').strip()
    sira_no = request.form.get('sira_no', '').strip()
    if not konu_adi:
        flash('Konu adı boş olamaz.', 'error')
        return redirect(url_for('hoca.hoca_konular'))
    try:
        sira_no = int(sira_no) if sira_no else 999
    except ValueError:
        sira_no = 999
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Konular SET KonuAdi=%s, SiraNo=%s WHERE KonuID=%s", (konu_adi, sira_no, konu_id))
    conn.commit()
    flash('Konu güncellendi.')
    return redirect(url_for('hoca.hoca_konular'))


@hoca_bp.route('/konu_sil/<int:konu_id>', methods=['POST'])
@hoca_required
def hoca_konu_sil(konu_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM SunumProgrami WHERE KonuID=%s", (konu_id,))
    cnt = cursor.fetchone()[0]
    if cnt > 0:
        flash(f'Bu konu {cnt} sunum slotunda kullanılıyor. Önce slotları silin.', 'error')
        return redirect(url_for('hoca.hoca_konular'))
    cursor.execute("DELETE FROM Konular WHERE KonuID=%s", (konu_id,))
    conn.commit()
    flash('Konu silindi.')
    return redirect(url_for('hoca.hoca_konular'))


# --- Dönem Yönetimi ---

@hoca_bp.route('/donemler')
@hoca_required
def hoca_donemler():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.DonemID, d.DonemAdi, d.Aktif,
               COUNT(DISTINCT b.BolumID) AS BolumSayisi
        FROM Donemler d
        LEFT JOIN Bolumler b ON b.DonemID = d.DonemID
        GROUP BY d.DonemID, d.DonemAdi, d.Aktif
        ORDER BY d.Aktif DESC, d.DonemID DESC
    """)
    donemler = cursor.fetchall()
    return render_template('hoca/hoca_donemler.html', donemler=donemler)


@hoca_bp.route('/donem_arsivle/<int:donem_id>', methods=['POST'])
@hoca_required
def hoca_donem_arsivle(donem_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Donemler SET Aktif=FALSE WHERE DonemID=%s", (donem_id,))
    conn.commit()
    flash('Dönem arşivlendi (pasif yapıldı). Veriler korunmaktadır.')
    return redirect(url_for('hoca.hoca_donemler'))


@hoca_bp.route('/donem_aktif_yap/<int:donem_id>', methods=['POST'])
@hoca_required
def hoca_donem_aktif_yap(donem_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Donemler SET Aktif=FALSE")
    cursor.execute("UPDATE Donemler SET Aktif=TRUE WHERE DonemID=%s", (donem_id,))
    conn.commit()
    flash('Dönem aktif yapıldı.')
    return redirect(url_for('hoca.hoca_donemler'))


# --- Takvim ---

@hoca_bp.route('/takvim')
@hoca_required
def hoca_takvim():
    return render_template('hoca/hoca_takvim.html')


# --- Hafta Yönetimi ---

@hoca_bp.route('/hafta_yonetimi')
@hoca_required
def hoca_hafta_yonetimi():
    bolum_id = request.args.get('bolum_id', '')
    tur = request.args.get('tur', 'Örgün')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi
        FROM HocaBolumler hb
        JOIN Bolumler b ON hb.BolumID=b.BolumID
        JOIN Donemler d ON b.DonemID=d.DonemID
        WHERE hb.HocaID=%s ORDER BY d.Aktif DESC, b.BolumAdi
    """, (session['hoca_id'],))
    bolumler = cursor.fetchall()
    slotlar = []
    if bolum_id:
        cursor.execute("""
            SELECT sp.SunumID, sp.HaftaNo, sp.OgretimTuru, sp.SunumTarihi, k.KonuID, k.KonuAdi, k.SiraNo
            FROM SunumProgrami sp JOIN Konular k ON sp.KonuID=k.KonuID
            WHERE sp.BolumID=%s ORDER BY sp.HaftaNo, k.SiraNo
        """, (bolum_id,))
        slotlar = cursor.fetchall()
    cursor.execute("SELECT KonuID, KonuAdi FROM Konular ORDER BY SiraNo, KonuAdi")
    tum_konular = cursor.fetchall()
    return render_template('hoca/hoca_hafta_yonetimi.html', bolumler=bolumler, slotlar=slotlar,
                           secili_bolum_id=bolum_id, tum_konular=tum_konular, tur=tur)


@hoca_bp.route('/sunum_hafta_guncelle', methods=['POST'])
@hoca_required
def hoca_sunum_hafta_guncelle():
    sunum_id = request.form.get('sunum_id')
    yeni_hafta = request.form.get('hafta_no', '').strip()
    bolum_id = request.form.get('bolum_id', '')
    if not yeni_hafta.isdigit():
        flash('Geçersiz hafta numarası.', 'error')
        return redirect(url_for('hoca.hoca_hafta_yonetimi', bolum_id=bolum_id))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE SunumProgrami SET HaftaNo=%s WHERE SunumID=%s", (int(yeni_hafta), sunum_id))
    conn.commit()
    flash('Hafta numarası güncellendi.')
    return redirect(url_for('hoca.hoca_hafta_yonetimi', bolum_id=bolum_id))


@hoca_bp.route('/sunum_tarih_guncelle', methods=['POST'])
@hoca_required
def hoca_sunum_tarih_guncelle():
    sunum_id = request.form.get('sunum_id')
    bolum_id = request.form.get('bolum_id', '')
    yeni_tarih_str = request.form.get('sunum_tarihi', '').strip()
    shift_others = request.form.get('shift_others') == '1'
    hafta_no = request.form.get('hafta_no', '')

    if not yeni_tarih_str:
        flash('Geçersiz tarih.', 'error')
        return redirect(url_for('hoca.hoca_hafta_yonetimi', bolum_id=bolum_id))

    try:
        yeni_tarih = datetime.strptime(yeni_tarih_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Geçersiz tarih formatı.', 'error')
        return redirect(url_for('hoca.hoca_hafta_yonetimi', bolum_id=bolum_id))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SunumTarihi, HaftaNo FROM SunumProgrami WHERE SunumID=%s", (sunum_id,))
    row = cursor.fetchone()
    eski_tarih = row.SunumTarihi if row else None
    current_hafta = row.HaftaNo if row else int(hafta_no)

    cursor.execute("UPDATE SunumProgrami SET SunumTarihi=%s WHERE SunumID=%s", (yeni_tarih, sunum_id))

    if shift_others and eski_tarih:
        fark = (yeni_tarih - eski_tarih).days
        if fark != 0:
            if bolum_id:
                cursor.execute("""
                    UPDATE SunumProgrami
                    SET SunumTarihi = SunumTarihi + make_interval(days => %s)
                    WHERE BolumID = %s AND HaftaNo > %s AND SunumTarihi IS NOT NULL
                """, (fark, bolum_id, current_hafta))
            else:
                cursor.execute("""
                    UPDATE SunumProgrami
                    SET SunumTarihi = SunumTarihi + make_interval(days => %s)
                    WHERE HaftaNo > %s AND SunumTarihi IS NOT NULL
                """, (fark, current_hafta))
            flash(f'Tarih güncellendi ve sonraki haftalar {fark} gün kaydırıldı.')
    elif shift_others and not eski_tarih:
        flash('Tarih güncellendi. (Mevcut tarih yoktu, kaydırma yapılamadı.)')
    else:
        flash('Sunum tarihi güncellendi.')

    conn.commit()
    return redirect(url_for('hoca.hoca_hafta_yonetimi', bolum_id=bolum_id))


@hoca_bp.route('/sunum_ekle', methods=['POST'])
@hoca_required
def hoca_sunum_ekle():
    bolum_id = request.form.get('bolum_id', '')
    konu_id = request.form.get('konu_id', '').strip()
    hafta_no = request.form.get('hafta_no', '').strip()
    ogretim_turu = request.form.get('ogretim_turu', 'Örgün')
    if not konu_id or not hafta_no.isdigit():
        flash('Konu veya hafta numarası geçersiz.', 'error')
        return redirect(url_for('hoca.hoca_hafta_yonetimi', bolum_id=bolum_id))
    conn = get_db_connection()
    cursor = conn.cursor()
    if bolum_id:
        cursor.execute("SELECT OgretimTuru FROM Bolumler WHERE BolumID=%s", (bolum_id,))
        b = cursor.fetchone()
        if b:
            ogretim_turu = b.OgretimTuru
    cursor.execute(
        "INSERT INTO SunumProgrami (KonuID, OgretimTuru, HaftaNo, BolumID) VALUES (%s, %s, %s, %s) RETURNING SunumID",
        (konu_id, ogretim_turu, int(hafta_no), bolum_id or None)
    )
    new_id_row = cursor.fetchone()
    if bolum_id:
        cursor.execute("""
            SELECT SunumTarihi FROM SunumProgrami
            WHERE BolumID=%s AND HaftaNo < %s AND SunumTarihi IS NOT NULL
            ORDER BY HaftaNo DESC LIMIT 1
        """, (bolum_id, int(hafta_no)))
        prev = cursor.fetchone()
        if prev and prev.SunumTarihi:
            auto_date = prev.SunumTarihi + timedelta(weeks=1)
            cursor.execute("UPDATE SunumProgrami SET SunumTarihi=%s WHERE SunumID=%s",
                           (auto_date, new_id_row.SunumID))
    conn.commit()
    flash('Sunum slotu eklendi.')
    return redirect(url_for('hoca.hoca_hafta_yonetimi', bolum_id=bolum_id))


@hoca_bp.route('/sunum_sil/<int:sunum_id>', methods=['POST'])
@hoca_required
def hoca_sunum_sil(sunum_id):
    bolum_id = request.form.get('bolum_id', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM SunumGorevlileri WHERE SunumID=%s", (sunum_id,))
    if cursor.fetchone()[0] > 0:
        flash('Bu slota atanmış öğrenci var. Önce atamayı kaldırın.', 'error')
        return redirect(url_for('hoca.hoca_hafta_yonetimi', bolum_id=bolum_id))
    cursor.execute("DELETE FROM KonuBasvurulari WHERE SunumID=%s", (sunum_id,))
    cursor.execute("DELETE FROM SoruBasvurulari WHERE SunumID=%s", (sunum_id,))
    cursor.execute("DELETE FROM SunumProgrami WHERE SunumID=%s", (sunum_id,))
    conn.commit()
    flash('Sunum slotu silindi.')
    return redirect(url_for('hoca.hoca_hafta_yonetimi', bolum_id=bolum_id))
