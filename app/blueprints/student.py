"""
Student Blueprint – Öğrenci paneli, başvurular, profil (SRP).
"""

from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, flash, abort, current_app, send_from_directory)
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

from db_manager import get_db_connection
from app.decorators import student_required, login_required
from app.utils import allowed_file, basvuru_acik_mi
from app.helpers import build_schedule_data

student_bp = Blueprint('student', __name__)

# Sunum dosyası (sunum/demo/kaynak) için izinli uzantılar
ALLOWED_SUNUM_EXTENSIONS = {
    'pdf', 'pptx', 'ppt', 'docx', 'doc', 'odp', 'odt',
    'mp4', 'webm', 'mov',
    'zip', 'rar', '7z',
    'png', 'jpg', 'jpeg',
}


def _is_sunan(cursor, sunum_id, current_no):
    """Verilen öğrenci numarası bu sunumun atanmış sahiplerinden mi?"""
    cursor.execute("""
        SELECT 1 FROM SunumGorevlileri sg
        JOIN Ogrenciler o ON o.OgrenciID = sg.OgrenciID
        WHERE sg.SunumID = %s AND o.OgrenciNo = %s
    """, (sunum_id, current_no))
    return cursor.fetchone() is not None


@student_bp.route('/panel')
@student_required
def student_panel():
    selected_tur = request.args.get('tur', 'Örgün')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sp.SunumID, sp.HaftaNo, k.KonuAdi, sp.SunumTarihi
        FROM SunumProgrami sp
        JOIN Konular k ON k.KonuID = sp.KonuID
        WHERE sp.OgretimTuru = %s
        ORDER BY sp.HaftaNo, k.SiraNo
    """, (selected_tur,))
    slots = cursor.fetchall()
    slot_ids = [s.SunumID for s in slots]

    if not slot_ids:
        return render_template('student/student_panel.html', schedule_data=[], selected_tur=selected_tur,
                               my_assignment=None, my_basvuru_count=0, my_soru_count=0,
                               my_applied_ids=set(), my_question_ids=set())

    schedule_data = build_schedule_data(slot_ids, slots)

    current_no = session['student_no']
    cursor.execute("""
        SELECT k.KonuAdi, sp.HaftaNo, sp.SunumID
        FROM SunumGorevlileri sg
        JOIN Ogrenciler o ON sg.OgrenciID = o.OgrenciID
        JOIN SunumProgrami sp ON sg.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE o.OgrenciNo = %s
    """, (current_no,))
    my_assignment = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM KonuBasvurulari WHERE Ogrenci1No = %s OR Ogrenci2No = %s", (current_no, current_no))
    my_basvuru_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM SoruBasvurulari WHERE OgrenciNo = %s", (current_no,))
    my_soru_count = cursor.fetchone()[0]

    cursor.execute("SELECT DISTINCT SunumID FROM KonuBasvurulari WHERE Ogrenci1No = %s OR Ogrenci2No = %s",
                   (current_no, current_no))
    my_applied_ids = {row.SunumID for row in cursor.fetchall()}

    cursor.execute("SELECT DISTINCT SunumID FROM SoruBasvurulari WHERE OgrenciNo = %s", (current_no,))
    my_question_ids = {row.SunumID for row in cursor.fetchall()}

    return render_template('student/student_panel.html',
                           schedule_data=schedule_data,
                           selected_tur=selected_tur,
                           my_assignment=my_assignment,
                           my_basvuru_count=my_basvuru_count,
                           my_soru_count=my_soru_count,
                           my_applied_ids=my_applied_ids,
                           my_question_ids=my_question_ids)


@student_bp.route('/topic/<int:sunum_id>')
@student_required
def student_topic_detail(sunum_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sp.SunumID, k.KonuAdi, sp.HaftaNo, sp.OgretimTuru
        FROM SunumProgrami sp JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE sp.SunumID = %s""", (sunum_id,))
    topic = cursor.fetchone()

    cursor.execute("SELECT o.AdSoyad, o.OgrenciNo FROM SunumGorevlileri sg JOIN Ogrenciler o ON o.OgrenciID=sg.OgrenciID WHERE sg.SunumID=%s", (sunum_id,))
    atananlar = cursor.fetchall()

    cursor.execute("SELECT BasvuruID, Ogrenci1No, Ogrenci2No, OncelikSirasi, ZamanDamgasi FROM KonuBasvurulari WHERE SunumID=%s ORDER BY OncelikSirasi", (sunum_id,))
    basvurular = cursor.fetchall()

    cursor.execute("""
        SELECT sb.SoruBasvuruID, o.OgrenciNo, o.AdSoyad, sb.IsApproved, sb.ZamanDamgasi, sb.RejectReason,
               sb.SoruIcerigi, sb.SunanOnayi, sb.SunanOnayTarihi, sb.SunanRedSebep
        FROM SoruBasvurulari sb
        JOIN Ogrenciler o ON o.OgrenciNo = sb.OgrenciNo
        WHERE sb.SunumID = %s
        ORDER BY sb.ZamanDamgasi ASC
    """, (sunum_id,))
    soru_soranlar = cursor.fetchall()

    current_no = session.get('student_no')
    my_topic_app = None
    my_question = None
    is_sunan = False
    if current_no:
        cursor.execute("""
            SELECT BasvuruID FROM KonuBasvurulari
            WHERE SunumID = %s AND (Ogrenci1No = %s OR Ogrenci2No = %s)
        """, (sunum_id, current_no, current_no))
        my_topic_app = cursor.fetchone()
        cursor.execute("SELECT SoruBasvuruID FROM SoruBasvurulari WHERE SunumID = %s AND OgrenciNo = %s",
                       (sunum_id, current_no))
        my_question = cursor.fetchone()
        is_sunan = _is_sunan(cursor, sunum_id, current_no)

    return render_template('student/student_topic_detail.html', topic=topic, atananlar=atananlar,
                           basvurular=basvurular, soru_soranlar=soru_soranlar,
                           my_topic_app=my_topic_app, my_question=my_question,
                           is_sunan=is_sunan)


@student_bp.route('/all_applications')
@student_required
def student_all_applications():
    current_no = session['student_no']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kb.BasvuruID, kb.Ogrenci1No, kb.Ogrenci2No, kb.OncelikSirasi, kb.ZamanDamgasi,
               k.KonuAdi, sp.HaftaNo, sp.SunumID,
               o1.AdSoyad AS Ad1, o2.AdSoyad AS Ad2,
               CASE WHEN sg.GorevID IS NOT NULL THEN TRUE ELSE FALSE END AS IsApproved
        FROM KonuBasvurulari kb
        JOIN SunumProgrami sp ON kb.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        LEFT JOIN Ogrenciler o1 ON o1.OgrenciNo = kb.Ogrenci1No
        LEFT JOIN Ogrenciler o2 ON o2.OgrenciNo = kb.Ogrenci2No
        LEFT JOIN Ogrenciler me ON me.OgrenciNo = %s
        LEFT JOIN SunumGorevlileri sg ON sg.SunumID = kb.SunumID AND sg.OgrenciID = me.OgrenciID
        WHERE kb.Ogrenci1No = %s OR kb.Ogrenci2No = %s
        ORDER BY kb.ZamanDamgasi ASC
    """, (current_no, current_no, current_no))
    applications = cursor.fetchall()
    return render_template('student/student_all_applications.html', applications=applications)


@student_bp.route('/questions')
@student_required
def student_questions():
    current_no = session['student_no']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sb.SoruBasvuruID, sb.OgrenciNo, o.AdSoyad, sb.ZamanDamgasi, sb.IsApproved, sb.RejectReason,
               k.KonuAdi, sp.HaftaNo, sp.SunumID
        FROM SoruBasvurulari sb
        JOIN Ogrenciler o ON sb.OgrenciNo = o.OgrenciNo
        JOIN SunumProgrami sp ON sb.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE sb.OgrenciNo = %s
        ORDER BY sb.ZamanDamgasi ASC
    """, (current_no,))
    questions = cursor.fetchall()
    return render_template('student/student_questions.html', questions=questions)


@student_bp.route('/profile/<student_no>')
@student_required
def student_profile(student_no):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT OgrenciID, OgrenciNo, AdSoyad, OgretimTuru, IsApproved FROM Ogrenciler WHERE OgrenciNo = %s", (student_no,))
    student = cursor.fetchone()

    if not student:
        flash("Öğrenci bulunamadı.")
        return redirect(url_for('student.student_panel'))

    cursor.execute("""
        SELECT k.KonuAdi, sp.HaftaNo, kb.ZamanDamgasi, sp.SunumID, sp.OgretimTuru
        FROM KonuBasvurulari kb
        JOIN SunumProgrami sp ON kb.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE kb.Ogrenci1No = %s OR kb.Ogrenci2No = %s
        ORDER BY kb.ZamanDamgasi
    """, (student_no, student_no))
    applications = cursor.fetchall()

    cursor.execute("""
        SELECT k.KonuAdi, sp.HaftaNo, sp.SunumID, sp.OgretimTuru
        FROM SunumGorevlileri sg
        JOIN SunumProgrami sp ON sg.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        JOIN Ogrenciler o ON sg.OgrenciID = o.OgrenciID
        WHERE o.OgrenciNo = %s
    """, (student_no,))
    assignment = cursor.fetchone()

    cursor.execute("""
        SELECT k.KonuAdi, sp.HaftaNo, sb.ZamanDamgasi, sp.SunumID, sp.OgretimTuru, sb.IsApproved, sb.RejectReason
        FROM SoruBasvurulari sb
        JOIN SunumProgrami sp ON sb.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE sb.OgrenciNo = %s
        ORDER BY sb.ZamanDamgasi
    """, (student_no,))
    questions = cursor.fetchall()

    return render_template('student/student_profile_view.html',
                           student=student,
                           applications=applications,
                           assignment=assignment,
                           questions=questions)


# --- BAŞVURU AKSİYONLARI ---

@student_bp.route('/apply_topic', methods=['POST'])
@student_required
def student_apply_topic():
    sunum_id = request.form.get('sunum_id')
    ortak_no = request.form.get('ortak_no', '').strip()
    current_no = session['student_no']

    if not sunum_id:
        flash("Geçersiz işlem.", "error")
        return redirect(url_for('student.student_panel'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT BolumID, DonemID FROM Ogrenciler WHERE OgrenciNo=%s", (current_no,))
    ogr_row = cursor.fetchone()
    if ogr_row and not basvuru_acik_mi(bolum_id=ogr_row.BolumID, donem_id=ogr_row.DonemID):
        flash("Başvuru süresi dolmuştur. Yeni başvuru yapılamaz.", "error")
        return redirect(url_for('student.student_panel') + f"#sunum-{sunum_id}")

    cursor.execute("""
        SELECT BasvuruID FROM KonuBasvurulari
        WHERE SunumID = %s AND (Ogrenci1No = %s OR Ogrenci2No = %s)
    """, (sunum_id, current_no, current_no))
    if cursor.fetchone():
        flash("Bu konuya zaten başvurdunuz!", "error")
        return redirect(url_for('student.student_panel') + f"#sunum-{sunum_id}")

    if ortak_no and ortak_no != current_no:
        cursor.execute("SELECT OgrenciNo FROM Ogrenciler WHERE OgrenciNo = %s", (ortak_no,))
        if not cursor.fetchone():
            flash("Girdiğiniz ortak öğrenci numarası sistemde bulunamadı!", "error")
            return redirect(url_for('student.student_panel') + f"#sunum-{sunum_id}")
    elif ortak_no == current_no:
        flash("Kendinizi ortak olarak ekleyemezsiniz!", "error")
        return redirect(url_for('student.student_panel') + f"#sunum-{sunum_id}")

    final_ortak = ortak_no if ortak_no else '0'

    cursor.execute("SELECT COALESCE(MAX(OncelikSirasi), 0) + 1 FROM KonuBasvurulari WHERE SunumID = %s", (sunum_id,))
    next_priority = cursor.fetchone()[0]

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO KonuBasvurulari (SunumID, Ogrenci1No, Ogrenci2No, OncelikSirasi, ZamanDamgasi)
        VALUES (%s, %s, %s, %s, %s)
    """, (sunum_id, current_no, final_ortak, next_priority, now_str))
    conn.commit()
    flash(f"Konu başvurunuz alındı! Sıra pozisyonunuz: {next_priority}. sıra")
    return redirect(url_for('student.student_panel') + f"#sunum-{sunum_id}")


@student_bp.route('/apply_question', methods=['POST'])
@student_required
def student_apply_question():
    sunum_id = request.form.get('sunum_id')
    current_no = session['student_no']

    if not sunum_id:
        flash("Geçersiz işlem.", "error")
        return redirect(url_for('student.student_panel'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SoruBasvuruID FROM SoruBasvurulari WHERE SunumID = %s AND OgrenciNo = %s",
                   (sunum_id, current_no))
    if cursor.fetchone():
        flash("Bu konuya zaten soru başvurusu yaptınız!", "error")
        return redirect(url_for('student.student_topic_detail', sunum_id=sunum_id))

    cursor.execute("""
        SELECT sg.SunumID FROM SunumGorevlileri sg
        JOIN Ogrenciler o ON sg.OgrenciID = o.OgrenciID
        WHERE sg.SunumID = %s AND o.OgrenciNo = %s
    """, (sunum_id, current_no))
    if cursor.fetchone():
        flash("Kendi sunum konunuza soru başvurusu yapamazsınız!", "error")
        return redirect(url_for('student.student_topic_detail', sunum_id=sunum_id))

    cursor.execute("SELECT COUNT(*) FROM SoruBasvurulari WHERE OgrenciNo = %s", (current_no,))
    soru_count = cursor.fetchone()[0]
    if soru_count >= 3:
        flash("3 soru hakkınızı kullandınız. Yeni başvuru yapamazsınız.", "error")
        return redirect(url_for('student.student_topic_detail', sunum_id=sunum_id))

    soru_icerigi = (request.form.get('soru_icerigi') or '').strip() or None
    if soru_icerigi and len(soru_icerigi) > 2000:
        soru_icerigi = soru_icerigi[:2000]

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO SoruBasvurulari (SunumID, OgrenciNo, ZamanDamgasi, SoruIcerigi)
        VALUES (%s, %s, %s, %s)
    """, (sunum_id, current_no, now_str, soru_icerigi))
    conn.commit()
    flash(f"Soru başvurunuz alındı! ({soru_count + 1}/3 soru hakkı kullanıldı)")
    return redirect(url_for('student.student_topic_detail', sunum_id=sunum_id))


@student_bp.route('/delete_application/<int:basvuru_id>', methods=['POST'])
@student_required
def student_delete_application(basvuru_id):
    current_no = session['student_no']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SunumID FROM KonuBasvurulari
        WHERE BasvuruID = %s AND (Ogrenci1No = %s OR Ogrenci2No = %s)
    """, (basvuru_id, current_no, current_no))
    row = cursor.fetchone()
    if not row:
        flash("Bu başvuru size ait değil veya bulunamadı!", "error")
        return redirect(url_for('student.student_all_applications'))

    cursor.execute("SELECT SunumID FROM SunumGorevlileri WHERE SunumID = %s", (row.SunumID,))
    if cursor.fetchone():
        flash("Bu konu zaten atanmış, iptal edemezsiniz!", "error")
        return redirect(url_for('student.student_all_applications'))

    cursor.execute("DELETE FROM KonuBasvurulari WHERE BasvuruID = %s", (basvuru_id,))
    conn.commit()
    flash("Konu başvurunuz iptal edildi.")
    return redirect(url_for('student.student_all_applications'))


@student_bp.route('/delete_question/<int:soru_id>', methods=['POST'])
@student_required
def student_delete_question(soru_id):
    current_no = session['student_no']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SoruBasvuruID, IsApproved FROM SoruBasvurulari WHERE SoruBasvuruID = %s AND OgrenciNo = %s",
                   (soru_id, current_no))
    row = cursor.fetchone()
    if not row:
        flash("Bu başvuru size ait değil!", "error")
        return redirect(url_for('student.student_questions'))

    cursor.execute("DELETE FROM SoruBasvurulari WHERE SoruBasvuruID = %s", (soru_id,))
    conn.commit()
    flash("Soru başvurunuz iptal edildi.")
    return redirect(url_for('student.student_questions'))


# --- PROFİL DÜZENLEME ---

@student_bp.route('/profile_edit', methods=['GET', 'POST'])
@student_required
def student_profile_edit():
    current_no = session['student_no']
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'change_password':
            from app.utils import change_password
            change_password('Ogrenciler', 'OgrenciNo', current_no,
                            request.form.get('old_password', ''),
                            request.form.get('new_password', ''),
                            request.form.get('new_password2', ''))

        elif action == 'change_photo':
            if 'kimlik_foto' in request.files:
                file = request.files['kimlik_foto']
                if file and file.filename and allowed_file(file.filename):
                    ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
                    fname = f"{uuid.uuid4().hex}.{ext}"
                    upload_path = os.path.join(student_bp.root_path, '..', '..', 'static', 'uploads', 'kimlikler')
                    upload_path = os.path.normpath(upload_path)
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, fname))
                    cursor.execute("UPDATE Ogrenciler SET KimlikFoto=%s WHERE OgrenciNo=%s", (fname, current_no))
                    conn.commit()
                    session['student_photo'] = fname
                    flash("Profil fotoğrafınız güncellendi.")
                else:
                    flash("Geçersiz dosya türü.", "error")

        return redirect(url_for('student.student_profile_edit'))

    cursor.execute("SELECT OgrenciNo, AdSoyad, OgretimTuru, KimlikFoto FROM Ogrenciler WHERE OgrenciNo=%s",
                   (current_no,))
    student = cursor.fetchone()
    return render_template('student/student_profile_edit.html', student=student)


# --- MESAJ GÖNDERME ---

@student_bp.route('/mesaj_gonder')
@student_required
def mesaj_gonder_page():
    return render_template('student/mesaj_gonder.html')


# =====================================================================
# SUNUM YÖNETİMİ – sadece sunumu yapan öğrenciler için
# Dosya yükleme (sunum/demo/kaynak) + soruya onay verme
# =====================================================================

@student_bp.route('/sunum/<int:sunum_id>/yonetim')
@student_required
def student_sunum_yonetim(sunum_id):
    """Sunum sahibinin kendi sunumunu yönettiği panel."""
    current_no = session['student_no']
    conn = get_db_connection()
    cursor = conn.cursor()
    if not _is_sunan(cursor, sunum_id, current_no):
        abort(403)

    cursor.execute("""
        SELECT sp.SunumID, k.KonuAdi, sp.HaftaNo, sp.OgretimTuru, sp.SunumTarihi
        FROM SunumProgrami sp JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE sp.SunumID = %s
    """, (sunum_id,))
    topic = cursor.fetchone()
    if not topic:
        abort(404)

    cursor.execute("""
        SELECT o.OgrenciNo, o.AdSoyad
        FROM SunumGorevlileri sg JOIN Ogrenciler o ON o.OgrenciID = sg.OgrenciID
        WHERE sg.SunumID = %s
    """, (sunum_id,))
    atananlar = cursor.fetchall()

    cursor.execute("""
        SELECT d.DosyaID, d.DosyaTipi, d.DosyaAdi, d.DosyaBoyutu, d.YuklemeTarihi, d.Aciklama,
               o.OgrenciNo AS YukleyenNo, o.AdSoyad AS YukleyenAd
        FROM SunumDosyalari d
        LEFT JOIN Ogrenciler o ON o.OgrenciID = d.YukleyenOgrenciID
        WHERE d.SunumID = %s
        ORDER BY d.YuklemeTarihi DESC
    """, (sunum_id,))
    dosyalar = cursor.fetchall()

    cursor.execute("""
        SELECT sb.SoruBasvuruID, sb.OgrenciNo, o.AdSoyad, sb.SoruIcerigi,
               sb.SunanOnayi, sb.SunanOnayTarihi, sb.SunanRedSebep,
               sb.IsApproved, sb.RejectReason, sb.ZamanDamgasi
        FROM SoruBasvurulari sb
        LEFT JOIN Ogrenciler o ON o.OgrenciNo = sb.OgrenciNo
        WHERE sb.SunumID = %s
        ORDER BY (sb.SunanOnayi IS NULL) DESC, sb.ZamanDamgasi ASC
    """, (sunum_id,))
    sorular = cursor.fetchall()

    return render_template('student/student_sunum_yonetim.html',
                           topic=topic, atananlar=atananlar,
                           dosyalar=dosyalar, sorular=sorular,
                           allowed_extensions=sorted(ALLOWED_SUNUM_EXTENSIONS),
                           max_size_mb=current_app.config.get('SUNUM_MAX_FILE_SIZE', 25 * 1024 * 1024) // (1024 * 1024))


@student_bp.route('/sunum/<int:sunum_id>/dosya_yukle', methods=['POST'])
@student_required
def student_sunum_dosya_yukle(sunum_id):
    from app.services.storage import get_storage, build_object_key, StorageError
    current_no = session['student_no']
    conn = get_db_connection()
    cursor = conn.cursor()
    if not _is_sunan(cursor, sunum_id, current_no):
        abort(403)

    dosya_tipi = (request.form.get('dosya_tipi') or '').strip()
    if dosya_tipi not in ('sunum', 'demo', 'kaynak'):
        flash('Geçersiz dosya tipi.', 'error')
        return redirect(url_for('student.student_sunum_yonetim', sunum_id=sunum_id))

    aciklama = (request.form.get('aciklama') or '').strip() or None
    file = request.files.get('dosya')
    if not file or not file.filename:
        flash('Dosya seçilmedi.', 'error')
        return redirect(url_for('student.student_sunum_yonetim', sunum_id=sunum_id))

    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in ALLOWED_SUNUM_EXTENSIONS:
        flash(f'Bu dosya tipi (.{ext}) desteklenmiyor.', 'error')
        return redirect(url_for('student.student_sunum_yonetim', sunum_id=sunum_id))

    # Boyut kontrolü (stream)
    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)
    max_size = current_app.config.get('SUNUM_MAX_FILE_SIZE', 25 * 1024 * 1024)
    if size > max_size:
        flash(f'Dosya boyutu {max_size // (1024 * 1024)} MB sınırını aşıyor.', 'error')
        return redirect(url_for('student.student_sunum_yonetim', sunum_id=sunum_id))

    storage = get_storage()
    key = build_object_key(sunum_id, dosya_tipi, file.filename)
    try:
        actual_size = storage.upload(file.stream, key)
    except StorageError as e:
        current_app.logger.error('Sunum dosyası yükleme hatası: %s', e)
        flash('Dosya yüklenirken hata oluştu.', 'error')
        return redirect(url_for('student.student_sunum_yonetim', sunum_id=sunum_id))

    cursor.execute("SELECT OgrenciID FROM Ogrenciler WHERE OgrenciNo=%s", (current_no,))
    ogr = cursor.fetchone()
    cursor.execute("""
        INSERT INTO SunumDosyalari (SunumID, YukleyenOgrenciID, DosyaTipi, DosyaAdi, DosyaYolu, DosyaBoyutu, Aciklama)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (sunum_id, ogr.OgrenciID if ogr else None, dosya_tipi, file.filename, key, actual_size, aciklama))
    conn.commit()
    flash(f"'{file.filename}' başarıyla yüklendi.")
    return redirect(url_for('student.student_sunum_yonetim', sunum_id=sunum_id))


@student_bp.route('/sunum/dosya/<int:dosya_id>/sil', methods=['POST'])
@student_required
def student_sunum_dosya_sil(dosya_id):
    from app.services.storage import get_storage
    current_no = session['student_no']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DosyaYolu, SunumID FROM SunumDosyalari WHERE DosyaID = %s", (dosya_id,))
    row = cursor.fetchone()
    if not row:
        abort(404)
    if not _is_sunan(cursor, row.SunumID, current_no):
        abort(403)
    try:
        get_storage().delete(row.DosyaYolu)
    except Exception as e:
        current_app.logger.warning('Storage silme hatası: %s', e)
    cursor.execute("DELETE FROM SunumDosyalari WHERE DosyaID=%s", (dosya_id,))
    conn.commit()
    flash('Dosya silindi.')
    return redirect(url_for('student.student_sunum_yonetim', sunum_id=row.SunumID))


@student_bp.route('/sunum/dosya/<int:dosya_id>/indir')
@login_required
def student_sunum_dosya_indir(dosya_id):
    """Auth check sonrası dosyayı indirir (local: stream, supabase: signed URL'e redirect).
    Tüm girilmiş rollerden erişilebilir (öğrenci, hoca, admin, kontrolcü)."""
    from app.services.storage import get_storage, StorageError
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DosyaYolu, DosyaAdi FROM SunumDosyalari WHERE DosyaID=%s", (dosya_id,))
    row = cursor.fetchone()
    if not row:
        abort(404)
    storage = get_storage()
    if storage.is_remote:
        try:
            url = storage.get_signed_url(row.DosyaYolu, expires_in=300)
        except StorageError as e:
            current_app.logger.error('Signed URL hatası: %s', e)
            abort(500)
        return redirect(url)
    try:
        directory, filename = storage.open_for_send(row.DosyaYolu)
    except StorageError:
        abort(404)
    return send_from_directory(directory, filename, as_attachment=True, download_name=row.DosyaAdi)


# =====================================================================
# GENEL SUNUM ARŞİVİ – tüm girilmiş roller (öğrenci, hoca, admin, kontrolcü)
# =====================================================================

@student_bp.route('/sunum/arsiv')
@login_required
def sunum_arsivi():
    """Yüklenen tüm sunum dosyalarını dönem/bölüm/tip filtreleriyle gösterir."""
    donem_id = request.args.get('donem_id', type=int)
    bolum_id = request.args.get('bolum_id', type=int)
    tip = (request.args.get('tip') or '').strip().lower()
    q = (request.args.get('q') or '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DonemID, DonemAdi FROM Donemler ORDER BY DonemID DESC")
    donemler = cursor.fetchall()
    cursor.execute("SELECT BolumID, BolumAdi, OgretimTuru FROM Bolumler ORDER BY BolumAdi")
    bolumler = cursor.fetchall()

    # Dinamik WHERE
    where_parts = []
    params = []
    if donem_id:
        where_parts.append("b.DonemID = %s"); params.append(donem_id)
    if bolum_id:
        where_parts.append("sp.BolumID = %s"); params.append(bolum_id)
    if tip in ('sunum', 'demo', 'kaynak'):
        where_parts.append("d.DosyaTipi = %s"); params.append(tip)
    if q:
        where_parts.append("(LOWER(d.DosyaAdi) LIKE %s OR LOWER(k.KonuAdi) LIKE %s)")
        like = f"%{q.lower()}%"
        params.extend([like, like])

    where_sql = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""

    cursor.execute(f"""
        SELECT d.DosyaID, d.DosyaTipi, d.DosyaAdi, d.DosyaBoyutu, d.YuklemeTarihi, d.Aciklama,
               d.SunumID, k.KonuAdi, sp.HaftaNo, sp.SunumTarihi, sp.OgretimTuru,
               b.BolumAdi, dn.DonemAdi,
               o.OgrenciNo AS YukleyenNo, o.AdSoyad AS YukleyenAd
        FROM SunumDosyalari d
        JOIN SunumProgrami sp ON sp.SunumID = d.SunumID
        JOIN Konular k ON k.KonuID = sp.KonuID
        LEFT JOIN Bolumler b ON b.BolumID = sp.BolumID
        LEFT JOIN Donemler dn ON dn.DonemID = b.DonemID
        LEFT JOIN Ogrenciler o ON o.OgrenciID = d.YukleyenOgrenciID
        {where_sql}
        ORDER BY d.YuklemeTarihi DESC
        LIMIT 500
    """, tuple(params))
    dosyalar = cursor.fetchall()

    # Her dosya için sunum ekibini topla (tek sorguda)
    sunum_ids = list({d.SunumID for d in dosyalar})
    ekipler = {}
    if sunum_ids:
        cursor.execute("""
            SELECT sg.SunumID, o.OgrenciNo, o.AdSoyad
            FROM SunumGorevlileri sg
            JOIN Ogrenciler o ON o.OgrenciID = sg.OgrenciID
            WHERE sg.SunumID = ANY(%s)
        """, (sunum_ids,))
        for r in cursor.fetchall():
            ekipler.setdefault(r.SunumID, []).append(r)

    # Tip dağılımı (üst kart)
    # Tip dağılımı (üst kart) — Bolumler join donem filtresi için gerekli
    cursor.execute(f"""
        SELECT d.DosyaTipi, COUNT(*) AS sayi
        FROM SunumDosyalari d
        JOIN SunumProgrami sp ON sp.SunumID = d.SunumID
        JOIN Konular k ON k.KonuID = sp.KonuID
        LEFT JOIN Bolumler b ON b.BolumID = sp.BolumID
        {where_sql}
        GROUP BY d.DosyaTipi
    """, tuple(params))
    tip_dagilimi = {r.DosyaTipi: r.sayi for r in cursor.fetchall()}

    return render_template('shared/sunum_arsivi.html',
                           dosyalar=dosyalar, ekipler=ekipler,
                           donemler=donemler, bolumler=bolumler,
                           tip_dagilimi=tip_dagilimi,
                           f_donem=donem_id, f_bolum=bolum_id, f_tip=tip, f_q=q)


@student_bp.route('/sunum/<int:sunum_id>/soru_onay/<int:basvuru_id>', methods=['POST'])
@student_required
def student_sunum_soru_onay(sunum_id, basvuru_id):
    """Sunum sahibinin soru başvurusuna onay/red vermesi (kontrolcüden bağımsız ön onay)."""
    current_no = session['student_no']
    action = request.form.get('action', 'approve')
    reject_reason = (request.form.get('reject_reason') or '').strip() or 'Sunum sahibi tarafından reddedildi.'
    conn = get_db_connection()
    cursor = conn.cursor()
    if not _is_sunan(cursor, sunum_id, current_no):
        abort(403)
    cursor.execute("SELECT SunumID FROM SoruBasvurulari WHERE SoruBasvuruID=%s", (basvuru_id,))
    sb = cursor.fetchone()
    if not sb or sb.SunumID != sunum_id:
        abort(404)

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if action == 'approve':
        # Onayla — bu sırada metin güncellenebilir (sunum sahibi sorulan gerçek soruyu yazabilir)
        soru_icerigi = (request.form.get('soru_icerigi') or '').strip()
        if soru_icerigi:
            soru_icerigi = soru_icerigi[:2000]
            cursor.execute("""
                UPDATE SoruBasvurulari
                   SET SunanOnayi=TRUE, SunanRedSebep=NULL, SunanOnayTarihi=%s,
                       SoruIcerigi=%s
                 WHERE SoruBasvuruID=%s
            """, (now_str, soru_icerigi, basvuru_id))
        else:
            cursor.execute("""
                UPDATE SoruBasvurulari
                   SET SunanOnayi=TRUE, SunanRedSebep=NULL, SunanOnayTarihi=%s
                 WHERE SoruBasvuruID=%s
            """, (now_str, basvuru_id))
        flash('Soruyu onayladınız.')
    elif action == 'edit_soru':
        # Sadece soru metnini güncelle, onay durumuna dokunma
        soru_icerigi = (request.form.get('soru_icerigi') or '').strip()[:2000] or None
        cursor.execute("""
            UPDATE SoruBasvurulari SET SoruIcerigi=%s WHERE SoruBasvuruID=%s
        """, (soru_icerigi, basvuru_id))
        flash('Soru metni güncellendi.')
    elif action == 'reject':
        cursor.execute("""
            UPDATE SoruBasvurulari
               SET SunanOnayi=FALSE, SunanRedSebep=%s, SunanOnayTarihi=%s
             WHERE SoruBasvuruID=%s
        """, (reject_reason[:255], now_str, basvuru_id))
        flash('Soruyu reddettiniz.')
    elif action == 'reset':
        cursor.execute("""
            UPDATE SoruBasvurulari
               SET SunanOnayi=NULL, SunanRedSebep=NULL, SunanOnayTarihi=NULL
             WHERE SoruBasvuruID=%s
        """, (basvuru_id,))
        flash('Onay durumu sıfırlandı.')
    else:
        flash('Geçersiz işlem.', 'error')
    conn.commit()
    return redirect(url_for('student.student_sunum_yonetim', sunum_id=sunum_id))
