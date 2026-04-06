"""
Student Blueprint – Öğrenci paneli, başvurular, profil (SRP).
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

from db_manager import get_db_connection
from app.decorators import student_required
from app.utils import allowed_file, basvuru_acik_mi
from app.helpers import build_schedule_data

student_bp = Blueprint('student', __name__)


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
        SELECT sb.SoruBasvuruID, o.OgrenciNo, o.AdSoyad, sb.IsApproved, sb.ZamanDamgasi, sb.RejectReason
        FROM SoruBasvurulari sb
        JOIN Ogrenciler o ON o.OgrenciNo = sb.OgrenciNo
        WHERE sb.SunumID = %s
        ORDER BY sb.ZamanDamgasi ASC
    """, (sunum_id,))
    soru_soranlar = cursor.fetchall()

    current_no = session.get('student_no')
    my_topic_app = None
    my_question = None
    if current_no:
        cursor.execute("""
            SELECT BasvuruID FROM KonuBasvurulari
            WHERE SunumID = %s AND (Ogrenci1No = %s OR Ogrenci2No = %s)
        """, (sunum_id, current_no, current_no))
        my_topic_app = cursor.fetchone()
        cursor.execute("SELECT SoruBasvuruID FROM SoruBasvurulari WHERE SunumID = %s AND OgrenciNo = %s",
                       (sunum_id, current_no))
        my_question = cursor.fetchone()

    return render_template('student/student_topic_detail.html', topic=topic, atananlar=atananlar,
                           basvurular=basvurular, soru_soranlar=soru_soranlar,
                           my_topic_app=my_topic_app, my_question=my_question)


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

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO SoruBasvurulari (SunumID, OgrenciNo, ZamanDamgasi)
        VALUES (%s, %s, %s)
    """, (sunum_id, current_no, now_str))
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
