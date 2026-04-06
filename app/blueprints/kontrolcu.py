"""
Kontrolcü Blueprint – Soru kontrolcüsü paneli ve işlemleri (SRP).
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from collections import OrderedDict

from db_manager import get_db_connection
from app.decorators import kontrolcu_required
from app.utils import kontrolcu_zaman_kontrol, try_send_email

kontrolcu_bp = Blueprint('kontrolcu', __name__)


@kontrolcu_bp.route('/panel')
@kontrolcu_required
def kontrolcu_panel():
    k_id = session['kontrolcu_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT BolumID FROM SoruKontrolculeri WHERE KontrolcuID=%s", (k_id,))
    k = cursor.fetchone()
    bolum_id = k.BolumID if k else None

    hafta_filter = request.args.get('hafta', '')

    query = """
        SELECT sb.SoruBasvuruID, sb.OgrenciNo, o.AdSoyad, sb.ZamanDamgasi,
               sb.IsApproved, sb.RejectReason,
               k.KonuAdi, sp.HaftaNo, sp.SunumID, sp.OgretimTuru, sp.SunumTarihi,
               k.KonuID
        FROM SoruBasvurulari sb
        JOIN SunumProgrami sp ON sb.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        LEFT JOIN Ogrenciler o ON sb.OgrenciNo = o.OgrenciNo
    """
    params = []
    where = []
    if bolum_id:
        where.append("sp.BolumID = %s")
        params.append(bolum_id)
    if hafta_filter:
        where.append("sp.HaftaNo = %s")
        params.append(hafta_filter)
    if where:
        query += " WHERE " + " AND ".join(where)
    query += " ORDER BY sp.HaftaNo, k.KonuAdi, sb.ZamanDamgasi"

    cursor.execute(query, params)
    sorular = cursor.fetchall()

    konular = OrderedDict()
    for s in sorular:
        key = (s.HaftaNo, s.SunumID, s.KonuAdi)
        if key not in konular:
            ok, msg = kontrolcu_zaman_kontrol(s.SunumTarihi)
            konular[key] = {
                'hafta': s.HaftaNo,
                'konu': s.KonuAdi,
                'sunum_id': s.SunumID,
                'ogretim_turu': s.OgretimTuru,
                'sunum_tarihi': s.SunumTarihi,
                'editable': ok,
                'zaman_mesaj': msg,
                'basvurular': []
            }
        konular[key]['basvurular'].append(s)

    q2 = "SELECT DISTINCT sp.HaftaNo FROM SunumProgrami sp"
    if bolum_id:
        q2 += " WHERE sp.BolumID=%s"
        cursor.execute(q2, (bolum_id,))
    else:
        cursor.execute(q2)
    haftalar = sorted([r.HaftaNo for r in cursor.fetchall()])

    return render_template('kontrolcu/kontrolcu_panel.html', konular=konular.values(),
                           sorular=sorular, haftalar=haftalar, secili_hafta=hafta_filter)


@kontrolcu_bp.route('/soru_guncelle', methods=['POST'])
@kontrolcu_required
def kontrolcu_soru_guncelle():
    basvuru_id = request.form.get('basvuru_id')
    action = request.form.get('action')
    reject_reason = request.form.get('reject_reason', 'Derse katılmadı veya soru sormadı.')
    hafta = request.form.get('hafta', '')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sp.SunumTarihi FROM SoruBasvurulari sb
        JOIN SunumProgrami sp ON sb.SunumID = sp.SunumID
        WHERE sb.SoruBasvuruID = %s
    """, (basvuru_id,))
    _st_row = cursor.fetchone()
    if _st_row:
        _ok, _msg = kontrolcu_zaman_kontrol(_st_row.SunumTarihi)
        if not _ok:
            flash(_msg, 'error')
            return redirect(url_for('kontrolcu.kontrolcu_panel', hafta=hafta))

    if action == 'approve':
        cursor.execute("SELECT sb2.SunumID FROM SoruBasvurulari sb2 WHERE sb2.SoruBasvuruID = %s", (basvuru_id,))
        row = cursor.fetchone()
        if row:
            cursor.execute("""
                SELECT COUNT(*) AS cnt FROM SoruBasvurulari
                WHERE SunumID = %s AND IsApproved = TRUE AND SoruBasvuruID != %s
            """, (row.SunumID, basvuru_id))
            cnt_row = cursor.fetchone()
            if cnt_row and cnt_row.cnt >= 6:
                flash('Bu konu için zaten 6 öğrenci onaylanmış. Onay vermek için önce başka birini reddedin.', 'error')
                return redirect(url_for('kontrolcu.kontrolcu_panel', hafta=hafta))
        cursor.execute("UPDATE SoruBasvurulari SET IsApproved=TRUE, RejectReason=NULL WHERE SoruBasvuruID=%s", (basvuru_id,))
    elif action == 'reject':
        cursor.execute("UPDATE SoruBasvurulari SET IsApproved=FALSE, RejectReason=%s WHERE SoruBasvuruID=%s",
                       (reject_reason, basvuru_id))
    conn.commit()

    try:
        cursor.execute("""
            SELECT sb.OgrenciNo, k.KonuAdi
            FROM SoruBasvurulari sb
            JOIN SunumProgrami sp ON sb.SunumID = sp.SunumID
            JOIN Konular k ON sp.KonuID = k.KonuID
            WHERE sb.SoruBasvuruID = %s
        """, (basvuru_id,))
        row = cursor.fetchone()
        if row:
            ogrno = row.OgrenciNo
            konu = row.KonuAdi
            if action == 'approve':
                subj = f"Soru Başvurunuz Onaylandı – {konu}"
                body = f"Merhaba,\n\n'{konu}' konusuna yaptığınız soru başvurusu onaylandı.\n\nİyi çalışmalar."
            else:
                subj = f"Soru Başvurunuz Reddedildi – {konu}"
                body = f"Merhaba,\n\n'{konu}' konusuna yaptığınız soru başvurusu reddedildi.\nSebep: {reject_reason}\n\nİyi çalışmalar."
            try_send_email(f"{ogrno}@{current_app.config['STUDENT_EMAIL_DOMAIN']}", subj, body)
    except Exception as e:
        current_app.logger.warning(f"Soru bildirim maili gönderilemedi: {e}")
    return redirect(url_for('kontrolcu.kontrolcu_panel', hafta=hafta))


@kontrolcu_bp.route('/soru_toplu_guncelle', methods=['POST'])
@kontrolcu_required
def kontrolcu_soru_toplu_guncelle():
    ids = request.form.getlist('ids[]')
    action = request.form.get('action')
    hafta = request.form.get('hafta', '')
    reject_reason = request.form.get('reject_reason', 'Toplu red işlemi.')
    if not ids:
        flash('Hiç kayıt seçilmedi.', 'error')
        return redirect(url_for('kontrolcu.kontrolcu_panel', hafta=hafta))
    conn = get_db_connection()
    cursor = conn.cursor()
    approved_count = 0
    rejected_count = 0
    skipped_count = 0
    time_blocked = 0
    for bid in ids:
        cursor.execute("""
            SELECT sp.SunumTarihi FROM SoruBasvurulari sb
            JOIN SunumProgrami sp ON sb.SunumID = sp.SunumID
            WHERE sb.SoruBasvuruID = %s
        """, (bid,))
        _st_row = cursor.fetchone()
        if _st_row:
            _ok, _msg = kontrolcu_zaman_kontrol(_st_row.SunumTarihi)
            if not _ok:
                time_blocked += 1
                continue
        if action == 'approve':
            cursor.execute("SELECT SunumID FROM SoruBasvurulari WHERE SoruBasvuruID=%s", (bid,))
            row = cursor.fetchone()
            if row:
                cursor.execute("""
                    SELECT COUNT(*) FROM SoruBasvurulari
                    WHERE SunumID=%s AND IsApproved=TRUE AND SoruBasvuruID!=%s
                """, (row.SunumID, bid))
                cnt = cursor.fetchone()[0]
                if cnt >= 6:
                    skipped_count += 1
                    continue
            cursor.execute("UPDATE SoruBasvurulari SET IsApproved=TRUE, RejectReason=NULL WHERE SoruBasvuruID=%s", (bid,))
            approved_count += 1
        elif action == 'reject':
            cursor.execute("UPDATE SoruBasvurulari SET IsApproved=FALSE, RejectReason=%s WHERE SoruBasvuruID=%s",
                           (reject_reason, bid))
            rejected_count += 1
    conn.commit()
    parts = []
    if approved_count:
        parts.append(f"{approved_count} onaylandı")
    if rejected_count:
        parts.append(f"{rejected_count} reddedildi")
    if skipped_count:
        parts.append(f"{skipped_count} atlandı (limit dolu)")
    if time_blocked:
        parts.append(f"{time_blocked} atlandı (süre dışı)")
    flash(', '.join(parts) + '.')
    return redirect(url_for('kontrolcu.kontrolcu_panel', hafta=hafta))


@kontrolcu_bp.route('/sifre_degistir', methods=['POST'])
@kontrolcu_required
def kontrolcu_sifre_degistir():
    from app.utils import change_password
    change_password('SoruKontrolculeri', 'KontrolcuID', session['kontrolcu_id'],
                    request.form.get('old_password', ''),
                    request.form.get('new_password', ''),
                    request.form.get('new_password2', ''))
    return redirect(url_for('kontrolcu.kontrolcu_panel'))
