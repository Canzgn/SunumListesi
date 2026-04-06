"""
Mesaj Blueprint – Mesajlaşma sistemi (öğrenci→hoca, öğrenci→admin, admin→hoca).
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from db_manager import get_db_connection
from app.decorators import login_required

mesaj_bp = Blueprint('mesaj', __name__)


def _get_sender_info():
    """Session'dan gönderen bilgilerini al."""
    role = session.get('user_role', '')
    if role == 'student':
        return role, session.get('student_no', ''), session.get('student_name', '')
    elif role == 'admin':
        return role, str(session.get('admin_id', '')), session.get('admin_name', '')
    elif role == 'hoca':
        return role, str(session.get('hoca_id', '')), session.get('hoca_name', '')
    elif role == 'kontrolcu':
        return role, str(session.get('kontrolcu_id', '')), session.get('kontrolcu_name', '')
    return '', '', ''


@mesaj_bp.route('/mesaj_gonder', methods=['POST'])
@login_required
def mesaj_gonder():
    """Mesaj gönder (herhangi bir kullanıcı)."""
    alici_rol = request.form.get('alici_rol', '').strip()
    alici_id = request.form.get('alici_id') or None
    konu = request.form.get('konu', '').strip()
    icerik = request.form.get('icerik', '').strip()
    redirect_url = request.form.get('redirect_url', '/')

    if not konu or not icerik:
        flash('Konu ve mesaj içeriği boş bırakılamaz.', 'error')
        return redirect(redirect_url)

    role, sender_id, sender_name = _get_sender_info()
    if not role:
        flash('Oturum hatası.', 'error')
        return redirect(redirect_url)

    # Öğrenci ise OgrenciID'yi bul
    gonderen_id = 0
    if role == 'student':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT OgrenciID FROM Ogrenciler WHERE OgrenciNo=%s", (sender_id,))
        row = cursor.fetchone()
        gonderen_id = row.OgrenciID if row else 0
    else:
        try:
            gonderen_id = int(sender_id)
        except (ValueError, TypeError):
            gonderen_id = 0

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Mesajlar (GonderenRol, GonderenID, GonderenAdi, AliciRol, AliciID, Konu, Icerik)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (role, gonderen_id, sender_name, alici_rol, alici_id, konu, icerik))
    conn.commit()
    flash('Mesajınız başarıyla gönderildi! ✉️')
    return redirect(redirect_url)


@mesaj_bp.route('/mesajlarim')
@login_required
def mesajlarim():
    """Gelen mesajları listele (admin veya hoca için)."""
    role = session.get('user_role', '')
    conn = get_db_connection()
    cursor = conn.cursor()

    if role == 'hoca':
        user_id = session.get('hoca_id')
        cursor.execute("""
            SELECT MesajID, GonderenRol, GonderenAdi, Konu, Icerik, Okundu, GonderimTarihi
            FROM Mesajlar
            WHERE AliciRol = 'hoca' AND (AliciID = %s OR AliciID IS NULL)
            ORDER BY GonderimTarihi DESC
        """, (user_id,))
    elif role == 'admin':
        user_id = session.get('admin_id')
        cursor.execute("""
            SELECT MesajID, GonderenRol, GonderenAdi, Konu, Icerik, Okundu, GonderimTarihi
            FROM Mesajlar
            WHERE AliciRol = 'admin' AND (AliciID = %s OR AliciID IS NULL)
            ORDER BY GonderimTarihi DESC
        """, (user_id,))
    else:
        flash('Erişim izniniz yok.', 'error')
        return redirect('/')

    mesajlar = cursor.fetchall()

    # Okunmamış sayısı
    okunmamis = sum(1 for m in mesajlar if not m.Okundu)

    return render_template('shared/mesajlar.html', mesajlar=mesajlar, okunmamis=okunmamis)


@mesaj_bp.route('/mesaj_oku/<int:mesaj_id>', methods=['POST'])
@login_required
def mesaj_oku(mesaj_id):
    """Mesajı okundu olarak işaretle."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Mesajlar SET Okundu=TRUE WHERE MesajID=%s", (mesaj_id,))
    conn.commit()
    return jsonify({'ok': True})


@mesaj_bp.route('/api/okunmamis_mesaj_sayisi')
@login_required
def okunmamis_mesaj_sayisi():
    """Okunmamış mesaj sayısını döndür (navbar'daki badge için)."""
    role = session.get('user_role', '')
    conn = get_db_connection()
    cursor = conn.cursor()

    if role == 'hoca':
        cursor.execute("""
            SELECT COUNT(*) FROM Mesajlar
            WHERE AliciRol='hoca' AND (AliciID=%s OR AliciID IS NULL) AND Okundu=FALSE
        """, (session.get('hoca_id'),))
    elif role == 'admin':
        cursor.execute("""
            SELECT COUNT(*) FROM Mesajlar
            WHERE AliciRol='admin' AND (AliciID=%s OR AliciID IS NULL) AND Okundu=FALSE
        """, (session.get('admin_id'),))
    else:
        return jsonify({'count': 0})

    count = cursor.fetchone()[0]
    return jsonify({'count': count})
