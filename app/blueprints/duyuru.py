"""
Duyuru (Announcement) Blueprint – SRP.
"""

from flask import Blueprint, request, redirect, url_for, session, flash, render_template, jsonify

from db_manager import get_db_connection
from app.decorators import admin_required, login_required

duyuru_bp = Blueprint('duyuru', __name__)


# ── Admin / Hoca duyuru yönetimi ───────────────────────────────

@duyuru_bp.route('/admin/duyurular')
@admin_required
def admin_duyurular():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Duyurular ORDER BY OlusturmaTarihi DESC")
    duyurular = cursor.fetchall()
    return render_template('duyuru/admin_duyurular.html', duyurular=duyurular)


@duyuru_bp.route('/admin/duyuru_ekle', methods=['POST'])
@admin_required
def admin_duyuru_ekle():
    baslik = request.form.get('baslik', '').strip()
    icerik = request.form.get('icerik', '').strip()
    roller = request.form.get('gosterilecek_roller', 'all')
    yapa = session.get('hoca_name') or session.get('admin_name') or 'Sistem'
    if not baslik:
        flash("Başlık boş olamaz.", "error")
        return redirect(url_for('duyuru.admin_duyurular'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Duyurular (Baslik, Icerik, YayinlayaciAdi, GosterilecekRoller) VALUES (%s,%s,%s,%s)",
        (baslik, icerik, str(yapa), roller)
    )
    conn.commit()
    flash("Duyuru yayınlandı.")
    return redirect(url_for('duyuru.admin_duyurular'))


@duyuru_bp.route('/admin/duyuru_sil/<int:duyuru_id>', methods=['POST'])
@admin_required
def admin_duyuru_sil(duyuru_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Duyurular WHERE DuyuruID=%s", (duyuru_id,))
    conn.commit()
    flash("Duyuru silindi.")
    return redirect(url_for('duyuru.admin_duyurular'))


# ── Öğrenci / Hoca salt okunur duyurular ───────────────────────

@duyuru_bp.route('/student/duyurular')
@login_required
def student_duyurular():
    role = session.get('user_role')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DuyuruID, Baslik, Icerik, YayinlayaciAdi,
               TO_CHAR(OlusturmaTarihi, 'DD.MM.YYYY HH24:MI') AS Tarih,
               GosterilecekRoller
        FROM Duyurular
        WHERE GosterilecekRoller='all' OR GosterilecekRoller=%s
        ORDER BY OlusturmaTarihi DESC
    """, (role,))
    duyurular = cursor.fetchall()
    return render_template('duyuru/student_duyurular.html', duyurular=duyurular)


# ── API – JSON duyurular (header badge) ────────────────────────

@duyuru_bp.route('/api/duyurular')
def api_duyurular():
    role = session.get('user_role', '')
    if not role:
        return jsonify([])
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DuyuruID, Baslik, Icerik, YayinlayaciAdi,
               TO_CHAR(OlusturmaTarihi, 'DD.MM.YYYY HH24:MI') AS Tarih
        FROM Duyurular
        WHERE GosterilecekRoller='all' OR GosterilecekRoller=%s
        ORDER BY OlusturmaTarihi DESC LIMIT 10
    """, (role,))
    rows = cursor.fetchall()
    return jsonify([{'id': r.DuyuruID, 'baslik': r.Baslik, 'icerik': r.Icerik,
                     'yayinlayici': r.YayinlayaciAdi, 'tarih': r.Tarih} for r in rows])
