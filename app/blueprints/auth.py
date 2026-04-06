"""
Auth Blueprint – Giriş, Kayıt, Çıkış (SRP).
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
import psycopg2.errors

from db_manager import get_db_connection
from app.utils import allowed_file

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        role = request.form.get('role')
        conn = get_db_connection()
        cursor = conn.cursor()
        # Sabit dummy hash – timing attack önlemi: kullanıcı bulunamasa bile hash karşılaştırması yapılır
        _dummy_hash = generate_password_hash('dummy')

        if role == 'admin':
            cursor.execute("SELECT AdminID, Password, IsApproved, AdSoyad, Username FROM Admins WHERE Username=%s", (user,))
            admin = cursor.fetchone()
            pw_ok = check_password_hash(admin.Password, pw) if (admin and admin.Password) else check_password_hash(_dummy_hash, pw)
            if admin and admin.IsApproved and pw_ok:
                session.permanent = True
                session['user_role'] = 'admin'
                session['admin_id'] = admin.AdminID
                session['admin_name'] = admin.AdSoyad or admin.Username
                return redirect(url_for('admin.admin_panel'))
            else:
                flash("Giriş başarısız! Bilgiler hatalı veya admin onayınız henüz verilmedi.")
        elif role == 'hoca':
            cursor.execute("SELECT HocaID, Password, IsApproved, AdSoyad FROM Hocalar WHERE Username=%s", (user,))
            hoca = cursor.fetchone()
            pw_ok = check_password_hash(hoca.Password, pw) if (hoca and hoca.Password) else check_password_hash(_dummy_hash, pw)
            if hoca and hoca.IsApproved and pw_ok:
                session.permanent = True
                session['user_role'] = 'hoca'
                session['hoca_id'] = hoca.HocaID
                session['hoca_name'] = hoca.AdSoyad or user
                return redirect(url_for('hoca.hoca_panel'))
            else:
                flash("Giriş başarısız! Bilgiler hatalı veya öğretmen onayınız henüz verilmedi.")
        elif role == 'kontrolcu':
            cursor.execute("SELECT KontrolcuID, Password, IsApproved, AdSoyad FROM SoruKontrolculeri WHERE Username=%s", (user,))
            k = cursor.fetchone()
            pw_ok = check_password_hash(k.Password, pw) if (k and k.Password) else check_password_hash(_dummy_hash, pw)
            if k and k.IsApproved and pw_ok:
                session.permanent = True
                session['user_role'] = 'kontrolcu'
                session['kontrolcu_id'] = k.KontrolcuID
                session['kontrolcu_name'] = k.AdSoyad or user
                return redirect(url_for('kontrolcu.kontrolcu_panel'))
            else:
                flash("Giriş başarısız! Bilgiler hatalı veya onayınız henüz verilmedi.")
        elif role == 'student':
            cursor.execute("SELECT OgrenciID, OgrenciNo, AdSoyad, OgretimTuru, IsApproved, KimlikFoto, Password FROM Ogrenciler WHERE OgrenciNo=%s AND IsApproved=TRUE", (user,))
            student = cursor.fetchone()
            pw_ok = check_password_hash(student.Password, pw) if (student and student.Password) else check_password_hash(_dummy_hash, pw)
            if student and pw_ok:
                session.permanent = True
                session['user_role'] = 'student'
                session['student_no'] = user
                session['student_name'] = student.AdSoyad
                session['student_photo'] = student.KimlikFoto
                return redirect(url_for('student.student_panel'))
            else:
                flash("Giriş başarısız! Öğrenci numarası veya şifre hatalı, ya da hesabınız onaylanmadı.")

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        reg_type = request.form.get('reg_type', 'student')
        ogr_no = request.form.get('ogrenci_no')
        ad_soyad = request.form.get('ad_soyad')
        pw = request.form.get('password')
        tur = request.form.get('ogretim_turu', 'Örgün')
        bolum_id = request.form.get('bolum_id') or None
        donem_id = request.form.get('donem_id') or None

        foto_filename = None
        if 'kimlik_foto' in request.files:
            file = request.files['kimlik_foto']
            if file and file.filename != '':
                if not allowed_file(file.filename):
                    flash('Sadece PNG, JPG, JPEG veya WEBP dosyası yükleyebilirsiniz!')
                    return redirect(url_for('auth.register'))
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}.{ext}"
                upload_path = os.path.join(auth_bp.root_path, '..', '..', 'static', 'uploads', 'kimlikler')
                upload_path = os.path.normpath(upload_path)
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, unique_filename))
                foto_filename = unique_filename

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if reg_type == 'admin':
                admin_bolum_id = request.form.get('admin_bolum_id') or None
                hashed_pw = generate_password_hash(pw)
                cursor.execute("INSERT INTO Admins (Username, Password, IsApproved, BolumID) VALUES (%s, %s, FALSE, %s)", (ogr_no, hashed_pw, admin_bolum_id))
                conn.commit()
                flash("Admin Başvurusu başarılı! Sisteme giriş için asıl adminin onayı bekleniyor.")
                return redirect(url_for('auth.login'))
            elif reg_type == 'student':
                cursor.execute("SELECT OgrenciID FROM Ogrenciler WHERE OgrenciNo = %s", (ogr_no,))
                existing_student = cursor.fetchone()

                if existing_student:
                    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    hashed_student_pw = generate_password_hash(pw) if pw else None
                    cursor.execute("""
                        UPDATE Ogrenciler
                        SET AdSoyad = %s, OgretimTuru = %s, IsApproved = FALSE,
                            KimlikFoto = %s, KayitTarihi = %s, Password = %s,
                            BolumID = %s, DonemID = %s
                        WHERE OgrenciNo = %s
                    """, (ad_soyad, tur, foto_filename, now_str, hashed_student_pw,
                          bolum_id, donem_id, ogr_no))
                    conn.commit()
                    flash("Öğrenci Kaydı başarılı! Sisteme giriş için admin onayı bekleniyor.")
                    return redirect(url_for('auth.login'))
                else:
                    if not bolum_id:
                        flash("Lütfen bölümünüzü seçin.", "error")
                    else:
                        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        hashed_student_pw = generate_password_hash(pw) if pw else None
                        cursor.execute("""
                            INSERT INTO Ogrenciler (OgrenciNo, AdSoyad, OgretimTuru, IsApproved,
                                                    KimlikFoto, KayitTarihi, Password, BolumID, DonemID)
                            VALUES (%s, %s, %s, FALSE, %s, %s, %s, %s, %s)
                        """, (ogr_no, ad_soyad, tur, foto_filename, now_str,
                              hashed_student_pw, bolum_id, donem_id))
                        conn.commit()
                        flash("Kaydınız alındı! Sisteme giriş için admin onayı bekleniyor.")
                        return redirect(url_for('auth.login'))
        except psycopg2.errors.UniqueViolation:
            flash("Dikkat: Bu kullanıcı numarası zaten sistemde kayıtlı!")
        except Exception as e:
            current_app.logger.error(f"Kayıt hatası: {e}")
            flash("Kayıt sırasında bir hata oluştu. Lütfen tekrar deneyin.")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.BolumID, b.BolumAdi, b.OgretimTuru, d.DonemAdi, d.DonemID
        FROM Bolumler b JOIN Donemler d ON b.DonemID = d.DonemID
        ORDER BY d.Aktif DESC, d.DonemAdi DESC, b.BolumAdi, b.OgretimTuru
    """)
    bolumler = cursor.fetchall()
    cursor.execute("SELECT DonemID, DonemAdi, Aktif FROM Donemler ORDER BY Aktif DESC, DonemAdi DESC")
    donemler = cursor.fetchall()

    return render_template('auth/register.html', bolumler=bolumler, donemler=donemler)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
