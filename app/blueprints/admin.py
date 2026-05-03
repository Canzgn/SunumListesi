"""
Admin Blueprint – Admin paneli, öğrenci yönetimi, atamalar, sorular, loglar (SRP).
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import generate_password_hash
from datetime import datetime
import psycopg2.errors
import secrets
from psycopg2.extras import execute_values

from db_manager import get_db_connection
from app.decorators import admin_required
from app.utils import get_admin_bolum_ids, get_admin_allowed_turs, log_islem, try_send_email
from app.helpers import (
    build_schedule_data,
    resolve_hafta_tarihi,
    shift_bolum_forward,
    shift_bolum_backward,
    cross_bolum_vize_apply,
    cross_bolum_tatil_apply,
    cross_bolum_vize_remove,
    cross_bolum_tatil_remove,
    get_donem_bolum_ids,
)

admin_bp = Blueprint('admin', __name__)


# --- SUNUM YÖNETİM PANELİ ---

@admin_bp.route('/panel')
@admin_required
def admin_panel():
    if session.get('user_role') == 'hoca':
        return redirect(url_for('hoca.hoca_sunum_panel'))

    allowed_turs = get_admin_allowed_turs()
    selected_tur = request.args.get('tur', allowed_turs[0] if allowed_turs else 'Örgün')
    if allowed_turs and selected_tur not in allowed_turs:
        selected_tur = allowed_turs[0]

    conn = get_db_connection()
    cursor = conn.cursor()

    admin_bolum_ids = get_admin_bolum_ids()

    if admin_bolum_ids:
        cursor.execute("""
            SELECT sp.SunumID, sp.HaftaNo, k.KonuAdi, sp.SunumTarihi
            FROM SunumProgrami sp
            JOIN Konular k ON k.KonuID = sp.KonuID
            WHERE sp.OgretimTuru = %s AND sp.BolumID = ANY(%s)
            ORDER BY sp.HaftaNo, k.SiraNo
        """, (selected_tur, admin_bolum_ids))
    else:
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
        cursor.execute("SELECT DonemID, DonemAdi AS YilLabel FROM Donemler ORDER BY DonemID DESC")
        donemler = cursor.fetchall()
        return render_template('admin/admin_panel.html', schedule_data=[], selected_tur=selected_tur,
                               donemler=donemler, allowed_turs=allowed_turs,
                               tatil_cadisi_sayisi=0, takvim_disi_sayisi=0,
                               tatil_tarihleri=[], akademik_bitis=None)

    schedule_data = build_schedule_data(slot_ids, slots)
    hafta_listesi = sorted(set(s.HaftaNo for s in slots))

    cursor.execute("""
        SELECT COUNT(*) FROM SunumProgrami sp
        JOIN TatilGunleri tg ON sp.sunumtarihi=tg.tarih
        JOIN Bolumler b ON b.bolumid=sp.bolumid
        WHERE b.donemid=tg.donemid
        AND sp.OgretimTuru = %s
    """, (selected_tur,))
    tatil_cadisi_sayisi = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM SunumProgrami sp
        JOIN Bolumler b ON sp.bolumid=b.bolumid
        JOIN Donemler d ON b.donemid=d.donemid
        WHERE d.donembitis IS NOT NULL AND sp.sunumtarihi > d.donembitis AND sp.sunumtarihi IS NOT NULL
        AND sp.OgretimTuru = %s
    """, (selected_tur,))
    takvim_disi_sayisi = cursor.fetchone()[0]

    cursor.execute("SELECT tarih FROM TatilGunleri ORDER BY tarih")
    tatil_tarihleri = [r.tarih for r in cursor.fetchall()]

    cursor.execute("SELECT MIN(d.donembitis) FROM Donemler d WHERE d.aktif=TRUE AND d.donembitis IS NOT NULL")
    ab_row = cursor.fetchone()
    akademik_bitis = ab_row[0] if ab_row else None

    cursor.execute("SELECT DonemID, DonemAdi AS YilLabel FROM Donemler ORDER BY DonemID DESC")
    donemler = cursor.fetchall()

    if admin_bolum_ids:
        cursor.execute(
            "SELECT DISTINCT ON (haftano) haftano, aciklama, islemyapan, hafta_tarihi FROM VizeHaftalari WHERE bolumid = ANY(%s) ORDER BY haftano",
            (admin_bolum_ids,)
        )
    else:
        cursor.execute("""
            SELECT DISTINCT ON (vh.haftano) vh.haftano, vh.aciklama, vh.islemyapan, vh.hafta_tarihi
            FROM VizeHaftalari vh
            JOIN Bolumler b ON b.bolumid = vh.bolumid WHERE b.ogretimturu = %s
            ORDER BY vh.haftano
        """, (selected_tur,))
    vize_rows_admin = cursor.fetchall()
    vize_haftalar = {r.haftano for r in vize_rows_admin}
    vize_meta = {r.haftano: {'aciklama': r.aciklama, 'islemyapan': r.islemyapan, 'hafta_tarihi': r.hafta_tarihi} for r in vize_rows_admin}

    if admin_bolum_ids:
        cursor.execute(
            "SELECT DISTINCT ON (haftano) haftano, aciklama, islemyapan, hafta_tarihi FROM TatilKaydirmaHaftalari WHERE bolumid = ANY(%s) ORDER BY haftano",
            (admin_bolum_ids,)
        )
    else:
        cursor.execute("""
            SELECT DISTINCT ON (tkh.haftano) tkh.haftano, tkh.aciklama, tkh.islemyapan, tkh.hafta_tarihi
            FROM TatilKaydirmaHaftalari tkh
            JOIN Bolumler b ON b.bolumid = tkh.bolumid WHERE b.ogretimturu = %s
            ORDER BY tkh.haftano
        """, (selected_tur,))
    tatilkaydir_rows_admin = cursor.fetchall()
    tatilkaydir_haftalar = {r.haftano for r in tatilkaydir_rows_admin}
    tatilkaydir_meta = {r.haftano: {'aciklama': r.aciklama, 'islemyapan': r.islemyapan, 'hafta_tarihi': r.hafta_tarihi} for r in tatilkaydir_rows_admin}

    # Tatil çakışması olan hafta numaraları
    cursor.execute("""
        SELECT DISTINCT sp.haftano FROM SunumProgrami sp
        JOIN TatilGunleri tg ON sp.sunumtarihi = tg.tarih
        JOIN Bolumler b ON b.bolumid = sp.bolumid
        WHERE b.donemid = tg.donemid AND sp.ogretimturu = %s
    """, (selected_tur,))
    tatil_cadisi_haftalari = {r.haftano for r in cursor.fetchall()}

    cursor.execute("SELECT tatilid, tarih, aciklama, eylemtipi FROM TatilGunleri ORDER BY tarih")
    tatil_gunleri = cursor.fetchall()

    cursor.execute("SELECT KonuID, KonuAdi FROM Konular ORDER BY SiraNo, KonuAdi")
    tum_konular = cursor.fetchall()

    # Bolümler selected_tur için (yeni slot ekle formu)
    if admin_bolum_ids:
        cursor.execute(
            "SELECT BolumID, BolumAdi FROM Bolumler WHERE BolumID = ANY(%s) AND OgretimTuru = %s ORDER BY BolumAdi",
            (admin_bolum_ids, selected_tur)
        )
    else:
        cursor.execute(
            "SELECT BolumID, BolumAdi FROM Bolumler WHERE OgretimTuru = %s ORDER BY BolumAdi",
            (selected_tur,)
        )
    panel_bolumler = cursor.fetchall()

    # Otomatik yerleştirme: bölüm bazlı overflow sayıları + aktif snapshot
    from app.helpers import auto_fit_active_snapshot
    panel_bolum_ids = [b.BolumID for b in panel_bolumler]
    overflow_per_bolum = {}
    autofit_per_bolum = {}
    if panel_bolum_ids:
        cursor.execute("""
            SELECT sp.BolumID, COUNT(*) AS cnt FROM SunumProgrami sp
            JOIN Bolumler b ON sp.BolumID = b.BolumID
            JOIN Donemler d ON b.DonemID = d.DonemID
            WHERE d.donembitis IS NOT NULL AND sp.SunumTarihi > d.donembitis
              AND sp.SunumTarihi IS NOT NULL AND sp.BolumID = ANY(%s)
            GROUP BY sp.BolumID
        """, (panel_bolum_ids,))
        for r in cursor.fetchall():
            overflow_per_bolum[r.BolumID] = r.cnt
        for bid in panel_bolum_ids:
            snap = auto_fit_active_snapshot(cursor, bid)
            if snap:
                autofit_per_bolum[bid] = {
                    'gecmisid': snap.gecmisid,
                    'olusturma_tarihi': snap.olusturma_tarihi,
                    'islemyapan': snap.islemyapan,
                }

    # Vize/tatil haftalarında slot yoksa boş header için placeholder satırı ekle
    slot_hafta_nos = {s['HaftaNo'] for s in schedule_data}
    for hafta_no in sorted((vize_haftalar | tatilkaydir_haftalar) - slot_hafta_nos):
        schedule_data.append({
            'SunumID': None, 'HaftaNo': hafta_no, 'SunumTarihi': None,
            'KonuAdi': None, 'Basvurular': [], 'Atananlar': [], 'Onaylanan': False,
            'OnaylananBasvuruID': None,
            'SoruSayisi': 0,
            'SoruOzet': {'toplam': 0, 'sunan_onayli': 0, 'hakem_onayli': 0, 'tam_onayli': 0},
            'Dosyalar': [],
        })
    schedule_data.sort(key=lambda x: x['HaftaNo'])

    # Hafta → tarih haritası (placeholder haftalara tarih göstermek için)
    hafta_tarih_map = {}
    for r in vize_rows_admin:
        if r.hafta_tarihi:
            hafta_tarih_map[r.haftano] = r.hafta_tarihi
    for r in tatilkaydir_rows_admin:
        if r.hafta_tarihi:
            hafta_tarih_map[r.haftano] = r.hafta_tarihi
    for s in schedule_data:
        if s.get('SunumTarihi'):
            hafta_tarih_map[s['HaftaNo']] = s['SunumTarihi']

    return render_template('admin/admin_panel.html',
                           schedule_data=schedule_data,
                           selected_tur=selected_tur,
                           donemler=donemler,
                           allowed_turs=allowed_turs,
                           hafta_listesi=hafta_listesi,
                           tatil_cadisi_sayisi=tatil_cadisi_sayisi,
                           takvim_disi_sayisi=takvim_disi_sayisi,
                           tatil_tarihleri=tatil_tarihleri,
                           akademik_bitis=akademik_bitis,
                           vize_haftalar=vize_haftalar,
                           vize_meta=vize_meta,
                           tatilkaydir_haftalar=tatilkaydir_haftalar,
                           tatilkaydir_meta=tatilkaydir_meta,
                           hafta_tarih_map=hafta_tarih_map,
                           tatil_cadisi_haftalari=tatil_cadisi_haftalari,
                           tatil_gunleri=tatil_gunleri,
                           tum_konular=tum_konular,
                           panel_bolumler=panel_bolumler,
                           overflow_per_bolum=overflow_per_bolum,
                           autofit_per_bolum=autofit_per_bolum)


# --- ÖĞRENCİ YÖNETİMİ ---

# --- PANEL HAFTA YÖNETİM ROUTE'LARı (Vize/Tatil - Admin panel inline) ---

@admin_bp.route('/panel_vize_ekle', methods=['POST'])
@admin_required
def admin_panel_vize_ekle():
    tur = request.form.get('tur', 'Örgün')
    hafta_no = request.form.get('hafta_no', '')
    if not hafta_no or not hafta_no.isdigit():
        flash('Geçersiz hafta numarası.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    hafta_no = int(hafta_no)
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()
    if admin_bolum_ids:
        cursor.execute(
            "SELECT BolumID FROM Bolumler WHERE BolumID = ANY(%s) AND OgretimTuru = %s",
            (admin_bolum_ids, tur)
        )
    else:
        cursor.execute("SELECT BolumID FROM Bolumler WHERE OgretimTuru = %s", (tur,))
    bolum_ids = [r.BolumID for r in cursor.fetchall()]
    if not bolum_ids:
        flash('Bu tür için bölüm bulunamadı.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    aciklama_v = request.form.get('aciklama', '').strip() or None
    islemyapan_v = session.get('admin_name', 'Admin')[:150]
    hafta_tarihi_str_v = request.form.get('hafta_tarihi', '').strip()
    # Tarih: form > ilk bölümün aynı hafta_no slotundan
    hafta_tarihi_v = resolve_hafta_tarihi(cursor, bolum_ids[0], hafta_no, hafta_tarihi_str_v)
    if hafta_tarihi_v is None:
        flash('Vize haftası için tarih belirlenemedi.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    # Tüm yetkili bölümleri aynı hafta tarihinde tarihe göre kaydır
    applied = cross_bolum_vize_apply(cursor, bolum_ids, hafta_tarihi_v, aciklama_v, islemyapan_v)
    conn.commit()
    flash(f'Vize haftası ({hafta_tarihi_v.strftime("%d.%m.%Y")}) {len(applied)} bölümde işaretlendi.', 'success')
    return redirect(url_for('admin.admin_panel', tur=tur))


@admin_bp.route('/panel_vize_sil', methods=['POST'])
@admin_required
def admin_panel_vize_sil():
    tur = request.form.get('tur', 'Örgün')
    hafta_no = request.form.get('hafta_no', '')
    if not hafta_no or not hafta_no.isdigit():
        flash('Geçersiz hafta numarası.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    hafta_no = int(hafta_no)
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()
    if admin_bolum_ids:
        cursor.execute(
            "SELECT BolumID FROM Bolumler WHERE BolumID = ANY(%s) AND OgretimTuru = %s",
            (admin_bolum_ids, tur)
        )
    else:
        cursor.execute("SELECT BolumID FROM Bolumler WHERE OgretimTuru = %s", (tur,))
    bolum_ids = [r.BolumID for r in cursor.fetchall()]
    if not bolum_ids:
        flash('Bölüm bulunamadı.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    hafta_tarihi_str = request.form.get('hafta_tarihi', '').strip()
    hafta_tarihi = resolve_hafta_tarihi(cursor, bolum_ids[0], hafta_no, hafta_tarihi_str)
    if hafta_tarihi is None:
        # Eski kayıtlar için fallback: bu hafta_no'da kayıtlı ilk vize hafta_tarihi'sini al
        cursor.execute(
            "SELECT hafta_tarihi FROM VizeHaftalari WHERE bolumid = ANY(%s) AND haftano = %s AND hafta_tarihi IS NOT NULL LIMIT 1",
            (bolum_ids, hafta_no)
        )
        r = cursor.fetchone()
        hafta_tarihi = r.hafta_tarihi if r else None
    if hafta_tarihi is None:
        flash('Vize haftası tarihi belirlenemedi (eski kayıt olabilir).', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    removed = cross_bolum_vize_remove(cursor, bolum_ids, hafta_tarihi)
    if not removed:
        conn.rollback()
        flash('Vize kaydı bulunamadı.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    conn.commit()
    flash(f'Vize haftası ({hafta_tarihi.strftime("%d.%m.%Y")}) {len(removed)} bölümden geri alındı.', 'success')
    return redirect(url_for('admin.admin_panel', tur=tur))


@admin_bp.route('/panel_tatil_kaydir', methods=['POST'])
@admin_required
def admin_panel_tatil_kaydir():
    tur = request.form.get('tur', 'Örgün')
    hafta_no = request.form.get('hafta_no', '')
    if not hafta_no or not hafta_no.isdigit():
        flash('Geçersiz hafta numarası.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    hafta_no = int(hafta_no)
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()
    if admin_bolum_ids:
        cursor.execute(
            "SELECT BolumID FROM Bolumler WHERE BolumID = ANY(%s) AND OgretimTuru = %s",
            (admin_bolum_ids, tur)
        )
    else:
        cursor.execute("SELECT BolumID FROM Bolumler WHERE OgretimTuru = %s", (tur,))
    bolum_ids = [r.BolumID for r in cursor.fetchall()]
    if not bolum_ids:
        flash('Bölüm bulunamadı.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    aciklama_t = request.form.get('aciklama', '').strip() or None
    islemyapan_t = session.get('admin_name', 'Admin')[:150]
    hafta_tarihi_str_t = request.form.get('hafta_tarihi', '').strip()
    holiday_date = resolve_hafta_tarihi(cursor, bolum_ids[0], hafta_no, hafta_tarihi_str_t)
    if holiday_date is None:
        flash('Tatil tarihi belirlenemedi.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    applied = cross_bolum_tatil_apply(cursor, bolum_ids, holiday_date, aciklama_t, islemyapan_t)
    conn.commit()
    flash(
        f'Tatil kaydırması ({holiday_date.strftime("%d.%m.%Y")}) — o haftada sunumu olan '
        f'{len(applied)} bölümde tüm hafta bir hafta ileri kaydırıldı.',
        'success'
    )
    return redirect(url_for('admin.admin_panel', tur=tur))


@admin_bp.route('/panel_tatil_kaydir_sil', methods=['POST'])
@admin_required
def admin_panel_tatil_kaydir_sil():
    tur = request.form.get('tur', 'Örgün')
    hafta_no = request.form.get('hafta_no', '')
    if not hafta_no or not hafta_no.isdigit():
        flash('Geçersiz hafta numarası.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    hafta_no = int(hafta_no)
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()
    if admin_bolum_ids:
        cursor.execute(
            "SELECT BolumID FROM Bolumler WHERE BolumID = ANY(%s) AND OgretimTuru = %s",
            (admin_bolum_ids, tur)
        )
    else:
        cursor.execute("SELECT BolumID FROM Bolumler WHERE OgretimTuru = %s", (tur,))
    bolum_ids = [r.BolumID for r in cursor.fetchall()]
    if not bolum_ids:
        flash('Bölüm bulunamadı.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    hafta_tarihi_str = request.form.get('hafta_tarihi', '').strip()
    holiday_date = resolve_hafta_tarihi(cursor, bolum_ids[0], hafta_no, hafta_tarihi_str)
    if holiday_date is None:
        cursor.execute(
            "SELECT hafta_tarihi FROM TatilKaydirmaHaftalari WHERE bolumid = ANY(%s) AND haftano = %s AND hafta_tarihi IS NOT NULL LIMIT 1",
            (bolum_ids, hafta_no)
        )
        r = cursor.fetchone()
        holiday_date = r.hafta_tarihi if r else None
    if holiday_date is None:
        flash('Tatil tarihi belirlenemedi (eski kayıt olabilir).', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    removed = cross_bolum_tatil_remove(cursor, bolum_ids, holiday_date)
    if not removed:
        conn.rollback()
        flash('Tatil kayıt bulunamadı.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    conn.commit()
    flash(f'Tatil kaydırması ({holiday_date.strftime("%d.%m.%Y")}) {len(removed)} bölümden geri alındı.', 'success')
    return redirect(url_for('admin.admin_panel', tur=tur))


@admin_bp.route('/panel_domino_uygula', methods=['POST'])
@admin_required
def admin_panel_domino_uygula():
    from datetime import datetime as dt
    tur = request.form.get('tur', 'Örgün')
    tatil_tarihi_str = request.form.get('tatil_tarihi', '')
    shift_days = int(request.form.get('shift_days', 7))
    try:
        tatil_tarihi = dt.strptime(tatil_tarihi_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        flash('Geçersiz tarih.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()
    if admin_bolum_ids:
        cursor.execute(
            "SELECT COUNT(*) FROM SunumProgrami WHERE bolumid = ANY(%s) AND sunumtarihi >= %s AND sunumtarihi IS NOT NULL",
            (admin_bolum_ids, tatil_tarihi)
        )
        etkilenen = cursor.fetchone()[0]
        cursor.execute(
            "UPDATE SunumProgrami SET sunumtarihi = sunumtarihi + make_interval(days=>%s) "
            "WHERE bolumid = ANY(%s) AND sunumtarihi >= %s AND sunumtarihi IS NOT NULL",
            (shift_days, admin_bolum_ids, tatil_tarihi)
        )
    else:
        cursor.execute(
            "SELECT COUNT(*) FROM SunumProgrami sp JOIN Bolumler b ON sp.bolumid=b.bolumid "
            "WHERE b.ogretimturu=%s AND sp.sunumtarihi >= %s AND sp.sunumtarihi IS NOT NULL",
            (tur, tatil_tarihi)
        )
        etkilenen = cursor.fetchone()[0]
        cursor.execute(
            "UPDATE SunumProgrami sp SET sunumtarihi = sunumtarihi + make_interval(days=>%s) "
            "FROM Bolumler b WHERE sp.bolumid=b.bolumid AND b.ogretimturu=%s "
            "AND sp.sunumtarihi >= %s AND sp.sunumtarihi IS NOT NULL",
            (shift_days, tur, tatil_tarihi)
        )
    conn.commit()
    flash(f'{etkilenen} slot {shift_days} gün ileri kaydırıldı.', 'success')
    return redirect(url_for('admin.admin_panel', tur=tur))


@admin_bp.route('/panel_auto_fit_uygula', methods=['POST'])
@admin_required
def admin_panel_auto_fit_uygula():
    from app.helpers import auto_fit_apply
    tur = request.form.get('tur', 'Örgün')
    bolum_id = request.form.get('bolum_id', '')
    if not bolum_id:
        flash('Bölüm seçilmedi.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    # Yetki: admin sadece sorumlu olduğu bölümlerde uygulayabilir
    admin_bolum_ids = get_admin_bolum_ids()
    if admin_bolum_ids is not None and int(bolum_id) not in admin_bolum_ids:
        flash('Bu bölüm üzerinde yetkiniz yok.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    islemyapan = session.get('admin_name', 'Admin')[:150]
    conn = get_db_connection()
    cursor = conn.cursor()
    gid, info = auto_fit_apply(cursor, bolum_id, islemyapan)
    if gid is None:
        conn.rollback()
        flash(info.get('error', 'Otomatik yerleştirme yapılamadı.'), 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    conn.commit()
    flash(
        f'Otomatik yerleştirme uygulandı: {info["overflow_count"]} sarkık konu '
        f'{info["weeks_used"]} haftaya dengeli dağıtıldı (haftada {info["min_per_week"]}-{info["max_per_week"]} sunum).',
        'success'
    )
    return redirect(url_for('admin.admin_panel', tur=tur))


@admin_bp.route('/panel_auto_fit_geri_al', methods=['POST'])
@admin_required
def admin_panel_auto_fit_geri_al():
    from app.helpers import auto_fit_undo
    tur = request.form.get('tur', 'Örgün')
    bolum_id = request.form.get('bolum_id', '')
    gecmisid = request.form.get('gecmisid', '')
    if not bolum_id or not gecmisid:
        flash('Geçersiz parametreler.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    admin_bolum_ids = get_admin_bolum_ids()
    if admin_bolum_ids is not None and int(bolum_id) not in admin_bolum_ids:
        flash('Bu bölüm üzerinde yetkiniz yok.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    conn = get_db_connection()
    cursor = conn.cursor()
    ok = auto_fit_undo(cursor, gecmisid, bolum_id)
    if not ok:
        conn.rollback()
        flash('Geri alma kaydı bulunamadı veya bu bölüme ait değil.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    conn.commit()
    flash('Otomatik yerleştirme geri alındı.', 'success')
    return redirect(url_for('admin.admin_panel', tur=tur))


@admin_bp.route('/panel_sunum_ekle', methods=['POST'])
@admin_required
def admin_panel_sunum_ekle():
    from datetime import timedelta
    tur = request.form.get('tur', 'Örgün')
    bolum_id = request.form.get('bolum_id', '')
    konu_id = request.form.get('konu_id', '').strip()
    hafta_no = request.form.get('hafta_no', '').strip()
    if not konu_id or not hafta_no.isdigit() or not bolum_id:
        flash('Konu, hafta numarası veya bölüm geçersiz.', 'error')
        return redirect(url_for('admin.admin_panel', tur=tur))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT OgretimTuru FROM Bolumler WHERE BolumID=%s", (bolum_id,))
    b = cursor.fetchone()
    ogretim_turu = b.OgretimTuru if b else tur
    cursor.execute(
        "INSERT INTO SunumProgrami (KonuID, OgretimTuru, HaftaNo, BolumID) VALUES (%s,%s,%s,%s) RETURNING SunumID",
        (konu_id, ogretim_turu, int(hafta_no), bolum_id)
    )
    new_row = cursor.fetchone()
    cursor.execute(
        "SELECT SunumTarihi FROM SunumProgrami WHERE BolumID=%s AND HaftaNo<%s AND SunumTarihi IS NOT NULL ORDER BY HaftaNo DESC LIMIT 1",
        (bolum_id, int(hafta_no))
    )
    prev = cursor.fetchone()
    if prev and prev.SunumTarihi:
        from datetime import timedelta as td
        cursor.execute("UPDATE SunumProgrami SET SunumTarihi=%s WHERE SunumID=%s",
                       (prev.SunumTarihi + td(weeks=1), new_row.SunumID))
    conn.commit()
    flash('Sunum slotu eklendi.', 'success')
    return redirect(url_for('admin.admin_panel', tur=tur))


# --- ÖĞRENCİ YÖNETİMİ ---

@admin_bp.route('/students')
@admin_required
def admin_students():
    status = request.args.get('status', 'all')
    type_filter = request.args.get('type', 'all')
    sort_by = request.args.get('sort', 'no')

    admin_bolum_ids = get_admin_bolum_ids()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT o.OgrenciID, o.OgrenciNo, o.AdSoyad, o.OgretimTuru, sp.HaftaNo, k.KonuAdi,
               sp.SunumID, sp.OgretimTuru AS SunumTuru,
               CASE WHEN sg.SunumID IS NOT NULL THEN 1 ELSE 0 END as HasSunum,
               (SELECT CASE WHEN kb.Ogrenci1No = o.OgrenciNo THEN kb.Ogrenci2No ELSE kb.Ogrenci1No END
                FROM KonuBasvurulari kb WHERE kb.Ogrenci1No = o.OgrenciNo OR kb.Ogrenci2No = o.OgrenciNo LIMIT 1) as GrupArkadasNo,
               o.IsApproved
        FROM Ogrenciler o
        LEFT JOIN SunumGorevlileri sg ON o.OgrenciID = sg.OgrenciID
        LEFT JOIN SunumProgrami sp ON sg.SunumID = sp.SunumID
        LEFT JOIN Konular k ON sp.KonuID = k.KonuID
    """
    where_clauses = []
    params = []
    if status == 'assigned':
        where_clauses.append("sg.SunumID IS NOT NULL")
    elif status == 'unassigned':
        where_clauses.append("sg.SunumID IS NULL")
    if type_filter != 'all':
        where_clauses.append("o.OgretimTuru = %s")
        params.append(type_filter)
    if admin_bolum_ids is not None:
        where_clauses.append("o.BolumID = ANY(%s)")
        params.append(admin_bolum_ids)

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    if sort_by == 'week':
        query += " ORDER BY HasSunum DESC, sp.HaftaNo ASC, k.KonuAdi ASC"
    else:
        query += " ORDER BY o.OgrenciNo ASC"

    cursor.execute(query, params)
    students = cursor.fetchall()

    if admin_bolum_ids is not None:
        cursor.execute("SELECT BolumID, BolumAdi, OgretimTuru FROM Bolumler WHERE BolumID = ANY(%s) ORDER BY BolumAdi", (admin_bolum_ids,))
    else:
        cursor.execute("SELECT BolumID, BolumAdi, OgretimTuru FROM Bolumler ORDER BY BolumAdi")
    bolumler = cursor.fetchall()
    return render_template('admin/admin_students.html', students=students, current_status=status,
                           current_type=type_filter, current_sort=sort_by, bolumler=bolumler)


# --- ADMİN YETKİ VE ONAY İŞLEMLERİ ---

@admin_bp.route('/manage_admins')
@admin_required
def manage_admins():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.AdminID, a.Username, a.AdSoyad, a.IsApproved, a.BolumID,
               b.BolumAdi, b.OgretimTuru AS BolumTuru
        FROM Admins a LEFT JOIN Bolumler b ON a.BolumID = b.BolumID
        ORDER BY a.IsApproved, a.Username
    """)
    all_admins = cursor.fetchall()
    cursor.execute("""
        SELECT ab.AdminID, b.BolumID, b.BolumAdi, b.OgretimTuru
        FROM AdminBolumler ab JOIN Bolumler b ON ab.BolumID = b.BolumID
        ORDER BY ab.AdminID, b.BolumAdi
    """)
    admin_bolum_rows = cursor.fetchall()
    admin_bolumler = {}
    for r in admin_bolum_rows:
        admin_bolumler.setdefault(r.AdminID, []).append(r)
    cursor.execute("SELECT BolumID, BolumAdi, OgretimTuru FROM Bolumler ORDER BY BolumAdi")
    all_bolumler = cursor.fetchall()
    return render_template('admin/manage_admins.html', admins=all_admins,
                           admin_bolumler=admin_bolumler, all_bolumler=all_bolumler)


@admin_bp.route('/approve_admin/<int:admin_id>', methods=['POST'])
@admin_required
def approve_admin(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Admins SET IsApproved = TRUE WHERE AdminID = %s", (admin_id,))
    cursor.execute("SELECT BolumID FROM Admins WHERE AdminID = %s", (admin_id,))
    admin_row = cursor.fetchone()
    if admin_row and admin_row.BolumID:
        cursor.execute("INSERT INTO AdminBolumler (AdminID, BolumID) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                       (admin_id, admin_row.BolumID))
    conn.commit()
    flash("Yönetici onayı verildi.")
    return redirect(url_for('admin.manage_admins'))


@admin_bp.route('/make_admin/<int:student_id>', methods=['POST'])
@admin_required
def make_admin(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT OgrenciNo FROM Ogrenciler WHERE OgrenciID = %s", (student_id,))
    res = cursor.fetchone()
    if res:
        try:
            temp_pw = secrets.token_urlsafe(8)
            hashed_pw = generate_password_hash(temp_pw)
            cursor.execute("INSERT INTO Admins (Username, Password, IsApproved) VALUES (%s, %s, TRUE)", (res[0], hashed_pw))
            conn.commit()
            flash(f"{res[0]} numaralı öğrenci artık bir admin! Geçici şifre: {temp_pw}")
        except Exception:
            flash("Bu öğrenci zaten admin listesinde.")
    return redirect(url_for('admin.admin_students'))


@admin_bp.route('/registered_users')
@admin_required
def admin_registered_users():
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()
    if admin_bolum_ids is not None:
        cursor.execute("""
            SELECT OgrenciID, OgrenciNo, AdSoyad, OgretimTuru, IsApproved, KimlikFoto, KayitTarihi
            FROM Ogrenciler
            WHERE AdSoyad IS NOT NULL AND AdSoyad != 'None' AND AdSoyad != ''
              AND BolumID = ANY(%s)
            ORDER BY IsApproved ASC, KayitTarihi DESC, OgrenciNo ASC
        """, (admin_bolum_ids,))
    else:
        cursor.execute("""
            SELECT OgrenciID, OgrenciNo, AdSoyad, OgretimTuru, IsApproved, KimlikFoto, KayitTarihi
            FROM Ogrenciler
            WHERE AdSoyad IS NOT NULL AND AdSoyad != 'None' AND AdSoyad != ''
            ORDER BY IsApproved ASC, KayitTarihi DESC, OgrenciNo ASC
        """)
    users = cursor.fetchall()
    return render_template('admin/admin_registered_users.html', users=users)


@admin_bp.route('/add_registered_user', methods=['POST'])
@admin_required
def add_registered_user():
    ogr_no = request.form.get('ogrenci_no')
    ad_soyad = request.form.get('ad_soyad')
    tur = request.form.get('ogretim_turu')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO Ogrenciler (OgrenciNo, AdSoyad, OgretimTuru, IsApproved, KayitTarihi)
            VALUES (%s, %s, %s, TRUE, %s)
        """, (ogr_no, ad_soyad, tur, now_str))
        conn.commit()
        flash(f"{ogr_no} numaralı öğrenci başarıyla eklendi.")
    except psycopg2.errors.UniqueViolation:
        flash("Bu numaraya sahip bir öğrenci zaten mevcut!")
    except Exception as e:
        current_app.logger.error(f"Öğrenci ekleme hatası: {e}")
        flash("Öğrenci eklenirken bir hata oluştu.")
    return redirect(url_for('admin.admin_registered_users'))


@admin_bp.route('/delete_registered_user/<int:student_id>', methods=['POST'])
@admin_required
def delete_registered_user(student_id):
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    if admin_bolum_ids:
        cursor.execute("SELECT BolumID FROM Ogrenciler WHERE OgrenciID = %s", (student_id,))
        ogr = cursor.fetchone()
        if not ogr or (ogr.BolumID and ogr.BolumID not in admin_bolum_ids):
            flash("Bu işlem için yetkiniz yok.")
            return redirect(url_for('admin.admin_registered_users'))

    try:
        cursor.execute("DELETE FROM SunumGorevlileri WHERE OgrenciID = %s", (student_id,))
        cursor.execute("SELECT OgrenciNo FROM Ogrenciler WHERE OgrenciID=%s", (student_id,))
        res = cursor.fetchone()
        if res:
            cursor.execute("DELETE FROM SoruBasvurulari WHERE OgrenciNo = %s", (res[0],))
            # KonuBasvurulari kasıtlı silinmiyor — başvuru geçmiş kaydıdır, öğrenci silinse de korunmalı
        cursor.execute("DELETE FROM Ogrenciler WHERE OgrenciID = %s", (student_id,))
        conn.commit()
        flash("Kullanıcı ve ilişkili tüm verileri başarıyla silindi.")
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Silme hatası: {e}")
        flash("Silme sırasında bir hata oluştu.")
    return redirect(url_for('admin.admin_registered_users'))


@admin_bp.route('/approve_student_account/<int:student_id>', methods=['POST'])
@admin_required
def approve_student_account(student_id):
    redirect_target = request.form.get('redirect_to', 'admin_students')
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    if admin_bolum_ids:
        cursor.execute("SELECT BolumID FROM Ogrenciler WHERE OgrenciID = %s", (student_id,))
        ogr = cursor.fetchone()
        if not ogr or (ogr.BolumID and ogr.BolumID not in admin_bolum_ids):
            flash("Bu işlem için yetkiniz yok.")
            return redirect(url_for('admin.admin_students'))

    cursor.execute("UPDATE Ogrenciler SET IsApproved = TRUE WHERE OgrenciID = %s", (student_id,))
    conn.commit()
    flash("Öğrenci hesabı onaylandı!")
    if redirect_target == 'registered_users':
        return redirect(url_for('admin.admin_registered_users'))
    return redirect(url_for('admin.admin_students'))


# --- ATAMA AKSİYONLARI ---

@admin_bp.route('/auto_assign', methods=['POST'])
@admin_required
def auto_assign():
    tur = request.form.get('tur', 'Örgün')
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    bolum_filter = "AND sp.BolumID = ANY(%s)" if admin_bolum_ids else ""
    params = [tur] + ([admin_bolum_ids] if admin_bolum_ids else [])
    cursor.execute(f"""
        SELECT DISTINCT ON (kb.SunumID) kb.SunumID, kb.Ogrenci1No, kb.Ogrenci2No
        FROM KonuBasvurulari kb
        JOIN SunumProgrami sp ON kb.SunumID = sp.SunumID
        WHERE sp.OgretimTuru = %s
          AND kb.SunumID NOT IN (SELECT DISTINCT SunumID FROM SunumGorevlileri)
          {bolum_filter}
        ORDER BY kb.SunumID, kb.OncelikSirasi ASC, kb.ZamanDamgasi ASC
    """, params)
    first_apps = cursor.fetchall()

    if first_apps:
        all_nos = list({no for row in first_apps for no in [row.Ogrenci1No, row.Ogrenci2No] if no and no != '0'})
        cursor.execute("SELECT OgrenciNo, OgrenciID FROM Ogrenciler WHERE OgrenciNo = ANY(%s)", (all_nos,))
        ogr_id_map = {r.OgrenciNo: r.OgrenciID for r in cursor.fetchall()}

        cursor.execute("UPDATE Ogrenciler SET IsApproved = TRUE WHERE OgrenciNo = ANY(%s)", (all_nos,))
        insert_values = []
        for row in first_apps:
            for no in [row.Ogrenci1No, row.Ogrenci2No]:
                if no and no != '0' and no in ogr_id_map:
                    insert_values.append((row.SunumID, ogr_id_map[no]))
        if insert_values:
            execute_values(cursor._cursor, "INSERT INTO SunumGorevlileri (SunumID, OgrenciID) VALUES %s ON CONFLICT DO NOTHING", insert_values)

    conn.commit()
    flash(f"{tur} öğretim türü için otomatik atama tamamlandı.")
    return redirect(url_for('admin.admin_panel', tur=tur))


@admin_bp.route('/clear_assignment', methods=['POST'])
@admin_required
def clear_assignment():
    s_id = request.form.get('sunum_id')
    tur = request.form.get('tur')
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    if admin_bolum_ids:
        cursor.execute("SELECT BolumID FROM SunumProgrami WHERE SunumID = %s", (s_id,))
        sp_row = cursor.fetchone()
        if not sp_row or sp_row.BolumID not in admin_bolum_ids:
            flash("Bu işlem için yetkiniz yok.")
            return redirect(url_for('admin.admin_panel', tur=tur))

    cursor.execute("SELECT k.KonuAdi FROM SunumProgrami sp JOIN Konular k ON k.KonuID=sp.KonuID WHERE sp.SunumID=%s", (s_id,))
    konu_row = cursor.fetchone()
    cursor.execute("DELETE FROM SunumGorevlileri WHERE SunumID = %s", (s_id,))
    conn.commit()
    log_islem('ONAY_KALDIR', sunum_id=int(s_id), konu_adi=konu_row.KonuAdi if konu_row else '')
    return redirect(url_for('admin.admin_panel', tur=tur) + f"#sunum-{s_id}")


@admin_bp.route('/clear_all', methods=['POST'])
@admin_required
def clear_all():
    tur = request.form.get('tur', 'Örgün')
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    if admin_bolum_ids:
        cursor.execute("""
            DELETE FROM SunumGorevlileri
            WHERE SunumID IN (SELECT SunumID FROM SunumProgrami WHERE OgretimTuru = %s AND BolumID = ANY(%s))
        """, (tur, admin_bolum_ids))
    else:
        cursor.execute("""
            DELETE FROM SunumGorevlileri
            WHERE SunumID IN (SELECT SunumID FROM SunumProgrami WHERE OgretimTuru = %s)
        """, (tur,))
    conn.commit()
    flash(f"{tur} öğretim türündeki tüm onaylar kaldırıldı.")
    return redirect(url_for('admin.admin_panel', tur=tur))


@admin_bp.route('/assign', methods=['POST'])
@admin_required
def admin_assign():
    s_id = request.form.get('sunum_id')
    b_id = request.form.get('basvuru_id')
    tur = request.form.get('tur')
    admin_bolum_ids = get_admin_bolum_ids()

    conn = get_db_connection()
    cursor = conn.cursor()

    if admin_bolum_ids:
        cursor.execute("SELECT BolumID FROM SunumProgrami WHERE SunumID = %s", (s_id,))
        sp_row = cursor.fetchone()
        if not sp_row or sp_row.BolumID not in admin_bolum_ids:
            flash("Bu işlem için yetkiniz yok.")
            return redirect(url_for('admin.admin_panel', tur=tur))

    cursor.execute("DELETE FROM SunumGorevlileri WHERE SunumID = %s", (s_id,))

    cursor.execute("SELECT Ogrenci1No, Ogrenci2No FROM KonuBasvurulari WHERE BasvuruID = %s", (b_id,))
    row = cursor.fetchone()
    atanan_nolar = []
    if row:
        for ogr_no in [row[0], row[1]]:
            if ogr_no and ogr_no != '0':
                cursor.execute("UPDATE Ogrenciler SET IsApproved = TRUE WHERE OgrenciNo = %s", (ogr_no,))
                cursor.execute("SELECT OgrenciID, AdSoyad FROM Ogrenciler WHERE OgrenciNo = %s", (ogr_no,))
                ogr_row = cursor.fetchone()
                if ogr_row:
                    cursor.execute("INSERT INTO SunumGorevlileri (SunumID, OgrenciID) VALUES (%s, %s)", (s_id, ogr_row[0]))
                    atanan_nolar.append(ogr_no)
    conn.commit()

    cursor.execute("SELECT k.KonuAdi FROM SunumProgrami sp JOIN Konular k ON k.KonuID=sp.KonuID WHERE sp.SunumID=%s", (s_id,))
    konu_row = cursor.fetchone()
    konu_adi = konu_row.KonuAdi if konu_row else ''
    log_islem('ONAY', sunum_id=s_id, konu_adi=konu_adi, detay=', '.join(atanan_nolar))

    for ogr_no in atanan_nolar:
        cursor.execute("SELECT AdSoyad FROM Ogrenciler WHERE OgrenciNo=%s", (ogr_no,))
        ogr = cursor.fetchone()
        ad = ogr.AdSoyad if ogr else ogr_no
        try_send_email(
            f"{ogr_no}@{current_app.config['STUDENT_EMAIL_DOMAIN']}",
            f"Sunum Ataması: {konu_adi}",
            f"Merhaba {ad},\n\n'{konu_adi}' konusuna sunum başvurunuz onaylandı.\n\nBaşarılar!"
        )

    return redirect(url_for('admin.admin_panel', tur=tur) + f"#sunum-{s_id}")


# --- SORULAR VE BAŞVURULAR ---

@admin_bp.route('/questions')
@admin_required
def admin_questions():
    sort_order = request.args.get('sort', 'konu')
    tur_filter = request.args.get('tur', '')
    hafta_filter = request.args.get('hafta', '')
    order_sql = "ASC" if sort_order == 'asc' else "DESC"
    if sort_order == 'konu':
        order_clause = "sp.HaftaNo ASC, k.KonuAdi ASC, sb.ZamanDamgasi DESC"
    else:
        order_clause = f"sb.ZamanDamgasi {order_sql}"

    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    bolum_filter = "AND sp.BolumID = ANY(%s)" if admin_bolum_ids else ""
    tur_sql = "AND sp.OgretimTuru = %s" if tur_filter else ""
    hafta_sql = "AND sp.HaftaNo = %s" if hafta_filter else ""

    params = []
    if admin_bolum_ids:
        params.append(admin_bolum_ids)
    if tur_filter:
        params.append(tur_filter)
    if hafta_filter:
        params.append(int(hafta_filter))

    cursor.execute(f"""
        WITH ranked AS (
            SELECT SoruBasvuruID,
                   ROW_NUMBER() OVER (PARTITION BY SunumID ORDER BY ZamanDamgasi ASC) AS pozisyon
            FROM SoruBasvurulari
            WHERE SunanOnayi IS DISTINCT FROM FALSE
        )
        SELECT sb.SoruBasvuruID, k.KonuAdi, sp.HaftaNo, sp.OgretimTuru,
               sb.OgrenciNo, o.AdSoyad, sb.ZamanDamgasi, sb.IsApproved, sb.RejectReason,
               sb.SunanOnayi, sb.SoruIcerigi, sp.SunumID,
               r.pozisyon
        FROM SoruBasvurulari sb
        LEFT JOIN ranked r ON r.SoruBasvuruID = sb.SoruBasvuruID
        JOIN SunumProgrami sp ON sb.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        LEFT JOIN Ogrenciler o ON sb.OgrenciNo = o.OgrenciNo
        WHERE 1=1 {bolum_filter} {tur_sql} {hafta_sql}
        ORDER BY {order_clause}
    """, params if params else None)
    applications = cursor.fetchall()

    cursor.execute("SELECT DISTINCT sp.HaftaNo FROM SunumProgrami sp ORDER BY sp.HaftaNo")
    hafta_listesi = [r.HaftaNo for r in cursor.fetchall()]

    return render_template('admin/admin_questions.html',
                           applications=applications,
                           current_sort=sort_order,
                           tur_filter=tur_filter,
                           hafta_filter=hafta_filter,
                           hafta_listesi=hafta_listesi)


@admin_bp.route('/soru_approve/<int:basvuru_id>', methods=['POST'])
@admin_required
def admin_soru_approve(basvuru_id):
    """Admin'in soru kaydını onaylaması veya reddetmesi (IsApproved)."""
    action = request.form.get('action', 'approve')
    reject_reason = (request.form.get('reject_reason') or '').strip() or 'Admin tarafından reddedildi.'
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SoruBasvuruID, SunanOnayi FROM SoruBasvurulari WHERE SoruBasvuruID=%s", (basvuru_id,))
    row = cursor.fetchone()
    if not row:
        abort(404)
    if action == 'approve':
        if row.SunanOnayi is not True:
            flash('Sunan henüz onaylamadı. Admin onayı yalnızca sunan onayından sonra verilebilir.', 'error')
            return redirect(request.referrer or url_for('admin.admin_questions'))
        cursor.execute(
            "UPDATE SoruBasvurulari SET IsApproved=TRUE, RejectReason=NULL WHERE SoruBasvuruID=%s",
            (basvuru_id,)
        )
        flash('Soru kaydı onaylandı.')
    elif action == 'reject':
        cursor.execute(
            "UPDATE SoruBasvurulari SET IsApproved=FALSE, RejectReason=%s WHERE SoruBasvuruID=%s",
            (reject_reason[:255], basvuru_id)
        )
        flash('Soru kaydı reddedildi.')
    else:  # reset
        cursor.execute(
            "UPDATE SoruBasvurulari SET IsApproved=NULL, RejectReason=NULL WHERE SoruBasvuruID=%s",
            (basvuru_id,)
        )
        flash('Soru kaydı durumu sıfırlandı.')
    conn.commit()
    return redirect(request.referrer or url_for('admin.admin_questions'))


@admin_bp.route('/all_applications')
@admin_required
def all_applications():
    sort_order = request.args.get('sort', 'asc')
    order_sql = "ASC" if sort_order == 'asc' else "DESC"

    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    bolum_filter = "AND sp.BolumID = ANY(%s)" if admin_bolum_ids else ""
    params = (admin_bolum_ids,) if admin_bolum_ids else ()
    cursor.execute(f"""
        SELECT kb.BasvuruID, k.KonuAdi, sp.HaftaNo, sp.OgretimTuru,
               kb.Ogrenci1No, kb.Ogrenci2No, kb.ZamanDamgasi, kb.OncelikSirasi, sp.SunumID
        FROM KonuBasvurulari kb
        JOIN SunumProgrami sp ON kb.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE 1=1 {bolum_filter}
        ORDER BY kb.ZamanDamgasi {order_sql}
    """, params)
    applications = cursor.fetchall()
    return render_template('admin/admin_applications.html', applications=applications, current_sort=sort_order)


# --- ÖĞRENCİ DETAY ---

@admin_bp.route('/student/<student_no>')
@admin_required
def student_detail(student_no):
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT AdSoyad, OgrenciNo, OgretimTuru, BolumID FROM Ogrenciler WHERE OgrenciNo = %s", (student_no,))
    student = cursor.fetchone()
    if not student:
        flash("Öğrenci bulunamadı.")
        return redirect(url_for('admin.admin_students'))

    if admin_bolum_ids and student.BolumID not in admin_bolum_ids:
        flash("Bu öğrenciyi görüntüleme yetkiniz yok.")
        return redirect(url_for('admin.admin_students'))

    cursor.execute("""
        SELECT k.KonuAdi, sp.HaftaNo, kb.OncelikSirasi, kb.ZamanDamgasi, sp.SunumID, sp.OgretimTuru
        FROM KonuBasvurulari kb
        JOIN SunumProgrami sp ON kb.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE kb.Ogrenci1No = %s OR kb.Ogrenci2No = %s
        ORDER BY kb.OncelikSirasi
    """, (student_no, student_no))
    applications = cursor.fetchall()

    cursor.execute("""
        SELECT k.KonuAdi, sp.HaftaNo
        FROM SunumGorevlileri sg
        JOIN SunumProgrami sp ON sg.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        JOIN Ogrenciler o ON sg.OgrenciID = o.OgrenciID
        WHERE o.OgrenciNo = %s
    """, (student_no,))
    assignment = cursor.fetchone()

    cursor.execute("""
        SELECT k.KonuAdi, sp.HaftaNo, sb.ZamanDamgasi, sp.SunumID, sp.OgretimTuru,
               sb.IsApproved, sb.RejectReason,
               sb.SunanOnayi, sb.SunanRedSebep, sb.SoruIcerigi
        FROM SoruBasvurulari sb
        JOIN SunumProgrami sp ON sb.SunumID = sp.SunumID
        JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE sb.OgrenciNo = %s
        ORDER BY sb.ZamanDamgasi
    """, (student_no,))
    questions = cursor.fetchall()

    return render_template('admin/student_detail.html',
                           student=student,
                           applications=applications,
                           assignment=assignment,
                           questions=questions)


@admin_bp.route('/topic/<int:sunum_id>')
@admin_required
def admin_topic_detail(sunum_id):
    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sp.SunumID, k.KonuAdi, sp.HaftaNo, sp.OgretimTuru, sp.BolumID
        FROM SunumProgrami sp JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE sp.SunumID = %s""", (sunum_id,))
    topic = cursor.fetchone()

    if topic and admin_bolum_ids and topic.BolumID not in admin_bolum_ids:
        flash("Bu konuyu görüntüleme yetkiniz yok.")
        return redirect(url_for('admin.admin_panel'))

    cursor.execute("SELECT o.AdSoyad, o.OgrenciNo FROM SunumGorevlileri sg JOIN Ogrenciler o ON o.OgrenciID=sg.OgrenciID WHERE sg.SunumID=%s", (sunum_id,))
    atananlar = cursor.fetchall()

    cursor.execute("SELECT BasvuruID, Ogrenci1No, Ogrenci2No, OncelikSirasi, ZamanDamgasi FROM KonuBasvurulari WHERE SunumID=%s ORDER BY OncelikSirasi", (sunum_id,))
    basvurular = cursor.fetchall()

    cursor.execute("""
        WITH ranked AS (
            SELECT SoruBasvuruID,
                   ROW_NUMBER() OVER (ORDER BY ZamanDamgasi ASC) AS pozisyon
            FROM SoruBasvurulari
            WHERE SunumID = %s AND SunanOnayi IS DISTINCT FROM FALSE
        )
        SELECT sb.SoruBasvuruID, o.OgrenciNo, o.AdSoyad, sb.IsApproved, sb.ZamanDamgasi, sb.RejectReason,
               sb.SunanOnayi, sb.SunanRedSebep, sb.SoruIcerigi, r.pozisyon
        FROM SoruBasvurulari sb
        LEFT JOIN ranked r ON r.SoruBasvuruID = sb.SoruBasvuruID
        JOIN Ogrenciler o ON o.OgrenciNo = sb.OgrenciNo
        WHERE sb.SunumID = %s
        ORDER BY sb.ZamanDamgasi ASC
    """, (sunum_id, sunum_id))
    soru_soranlar = cursor.fetchall()

    return render_template('admin/admin_topic_detail.html', topic=topic, atananlar=atananlar,
                           basvurular=basvurular, soru_soranlar=soru_soranlar)


@admin_bp.route('/topic/update_question_status', methods=['POST'])
@admin_required
def update_question_status():
    basvuru_id = request.form.get('basvuru_id')
    sunum_id = request.form.get('sunum_id')
    action = request.form.get('action')
    reject_reason = request.form.get('reject_reason', 'Derse katılmadı veya soru sormadı.')

    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    if admin_bolum_ids:
        cursor.execute("SELECT BolumID FROM SunumProgrami WHERE SunumID = %s", (sunum_id,))
        sp_row = cursor.fetchone()
        if not sp_row or sp_row.BolumID not in admin_bolum_ids:
            flash("Bu işlem için yetkiniz yok.")
            return redirect(url_for('admin.admin_panel'))

    if action == 'approve':
        cursor.execute("SELECT SunanOnayi FROM SoruBasvurulari WHERE SoruBasvuruID = %s", (basvuru_id,))
        sb_row = cursor.fetchone()
        if not sb_row or sb_row.SunanOnayi is not True:
            flash('Sunan henüz onaylamadı. Admin onayı yalnızca sunan onayından sonra verilebilir.', 'error')
            return redirect(url_for('admin.admin_topic_detail', sunum_id=sunum_id))
        cursor.execute("UPDATE SoruBasvurulari SET IsApproved = TRUE, RejectReason = NULL WHERE SoruBasvuruID = %s", (basvuru_id,))
        flash("Soru hakkı tekrar verildi / Onaylandı.")
    elif action == 'reject':
        cursor.execute("UPDATE SoruBasvurulari SET IsApproved = FALSE, RejectReason = %s WHERE SoruBasvuruID = %s", (reject_reason, basvuru_id,))
        flash("Öğrencinin soru sorma hakkı iptal edildi.")

    conn.commit()
    return redirect(url_for('admin.admin_topic_detail', sunum_id=sunum_id))


# --- LOGLAR ---

@admin_bp.route('/logs')
@admin_required
def admin_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT LogID, Eylem, SunumID, KonuAdi, YapaAdi, Detay,
               TO_CHAR(ZamanDamgasi, 'DD.MM.YYYY HH24:MI:SS') AS Zaman
        FROM IslemLoglari ORDER BY ZamanDamgasi DESC LIMIT 200
    """)
    logs = cursor.fetchall()
    return render_template('admin/admin_logs.html', logs=logs)


# --- DÖNEM KİLİDİ ---

@admin_bp.route('/donem_kilidi', methods=['POST'])
@admin_required
def admin_donem_kilidi():
    donem_id = request.form.get('donem_id')
    bitis = request.form.get('basvuru_bitis', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    if bitis:
        cursor.execute("UPDATE Donemler SET BasvuruBitis=%s WHERE DonemID=%s", (bitis, donem_id))
        flash("Başvuru bitiş tarihi ayarlandı.")
    else:
        cursor.execute("UPDATE Donemler SET BasvuruBitis=NULL WHERE DonemID=%s", (donem_id,))
        flash("Başvuru bitiş tarihi kaldırıldı (süresiz açık).")
    conn.commit()
    return redirect(request.referrer or url_for('admin.admin_panel'))


# --- ÖĞRENCİ BÖLÜM DEĞİŞTİRME ---

@admin_bp.route('/student/bolum_degistir', methods=['POST'])
@admin_required
def admin_student_bolum_degistir():
    student_id = request.form.get('student_id')
    yeni_bolum_id = request.form.get('yeni_bolum_id') or None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Ogrenciler SET BolumID=%s WHERE OgrenciID=%s", (yeni_bolum_id, student_id))
    conn.commit()
    if yeni_bolum_id:
        cursor.execute("SELECT BolumAdi FROM Bolumler WHERE BolumID=%s", (yeni_bolum_id,))
        b = cursor.fetchone()
        flash(f"Öğrenci bölümü '{b.BolumAdi}' olarak güncellendi.")
    else:
        flash("Öğrencinin bölüm ataması kaldırıldı.")
    return redirect(request.referrer or url_for('admin.admin_students'))


# --- ADMİN ŞİFRE DEĞİŞTİRME ---

@admin_bp.route('/update_hafta_tarihi', methods=['POST'])
@admin_required
def update_hafta_tarihi():
    hafta_no = request.form.get('hafta_no', type=int)
    tur = request.form.get('tur')
    yeni_tarih = request.form.get('yeni_tarih', '').strip()

    if not hafta_no or not tur:
        flash("Geçersiz parametre.")
        return redirect(request.referrer or url_for('admin.admin_panel'))

    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    tarih_val = yeni_tarih if yeni_tarih else None

    if admin_bolum_ids:
        cursor.execute("""
            UPDATE SunumProgrami SET SunumTarihi = %s
            WHERE HaftaNo = %s AND OgretimTuru = %s AND BolumID = ANY(%s)
        """, (tarih_val, hafta_no, tur, admin_bolum_ids))
    else:
        cursor.execute("""
            UPDATE SunumProgrami SET SunumTarihi = %s
            WHERE HaftaNo = %s AND OgretimTuru = %s
        """, (tarih_val, hafta_no, tur))

    conn.commit()
    if tarih_val:
        flash(f"{hafta_no}. haftanın tarihi güncellendi.")
    else:
        flash(f"{hafta_no}. haftanın tarihi kaldırıldı.")
    return redirect(url_for('admin.admin_panel', tur=tur) + f"#hafta-{hafta_no}")


@admin_bp.route('/move_konu', methods=['POST'])
@admin_required
def move_konu():
    sunum_id = request.form.get('sunum_id', type=int)
    yeni_hafta_no = request.form.get('yeni_hafta_no', type=int)
    tur = request.form.get('tur')

    if not sunum_id or not yeni_hafta_no or not tur:
        flash("Geçersiz parametre.")
        return redirect(request.referrer or url_for('admin.admin_panel'))

    admin_bolum_ids = get_admin_bolum_ids()
    conn = get_db_connection()
    cursor = conn.cursor()

    if admin_bolum_ids:
        cursor.execute("SELECT BolumID FROM SunumProgrami WHERE SunumID = %s", (sunum_id,))
        sp_row = cursor.fetchone()
        if not sp_row or sp_row.BolumID not in admin_bolum_ids:
            flash("Bu işlem için yetkiniz yok.")
            return redirect(url_for('admin.admin_panel', tur=tur))

    # Hedef haftanın tarihini bul (aynı tur ve bölümden)
    if admin_bolum_ids:
        cursor.execute("""
            SELECT SunumTarihi FROM SunumProgrami
            WHERE HaftaNo = %s AND OgretimTuru = %s AND BolumID = ANY(%s) AND SunumTarihi IS NOT NULL
            LIMIT 1
        """, (yeni_hafta_no, tur, admin_bolum_ids))
    else:
        cursor.execute("""
            SELECT SunumTarihi FROM SunumProgrami
            WHERE HaftaNo = %s AND OgretimTuru = %s AND SunumTarihi IS NOT NULL
            LIMIT 1
        """, (yeni_hafta_no, tur))
    hedef = cursor.fetchone()
    yeni_tarih = hedef.SunumTarihi if hedef else None

    cursor.execute("""
        UPDATE SunumProgrami SET HaftaNo = %s, SunumTarihi = %s WHERE SunumID = %s
    """, (yeni_hafta_no, yeni_tarih, sunum_id))
    conn.commit()

    cursor.execute("SELECT k.KonuAdi FROM SunumProgrami sp JOIN Konular k ON k.KonuID = sp.KonuID WHERE sp.SunumID = %s", (sunum_id,))
    konu_row = cursor.fetchone()
    flash(f"'{konu_row.KonuAdi if konu_row else ''}' konusu {yeni_hafta_no}. haftaya taşındı.")
    return redirect(url_for('admin.admin_panel', tur=tur) + f"#sunum-{sunum_id}")


@admin_bp.route('/sifre_degistir', methods=['POST'])
@admin_required
def admin_sifre_degistir():
    from app.utils import change_password
    role = session['user_role']
    if role == 'hoca':
        change_password('Hocalar', 'HocaID', session['hoca_id'],
                        request.form.get('old_password', ''),
                        request.form.get('new_password', ''),
                        request.form.get('new_password2', ''))
    else:
        change_password('Admins', 'AdminID', session['admin_id'],
                        request.form.get('old_password', ''),
                        request.form.get('new_password', ''),
                        request.form.get('new_password2', ''))
    return redirect(request.referrer or url_for('admin.admin_panel'))

@admin_bp.route('/hafta_yonetimi')
@admin_required
def admin_hafta_yonetimi():
    return redirect(url_for('hoca.hoca_hafta_yonetimi'))
