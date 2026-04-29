"""
Paylaşılan veri dönüşüm fonksiyonları – DRY & SRP.
admin_panel, student_panel, hoca_sunum_panel'de
tekrar eden schedule_data oluşturma mantığı burada merkezileştirilmiştir.
"""

from db_manager import get_db_connection


def build_schedule_data(slot_ids, slots):
    """Slot ID'leri ve slot listesinden schedule_data sözlük listesi oluşturur."""
    if not slot_ids:
        return []

    conn = get_db_connection()
    cursor = conn.cursor()

    # Atananlar
    cursor.execute("""
        SELECT sg.SunumID, o.AdSoyad, o.OgrenciNo
        FROM SunumGorevlileri sg
        JOIN Ogrenciler o ON o.OgrenciID = sg.OgrenciID
        WHERE sg.SunumID = ANY(%s)
    """, (slot_ids,))
    atananlar_map = {}
    for row in cursor.fetchall():
        atananlar_map.setdefault(row.SunumID, []).append(row)

    # Başvurular
    cursor.execute("""
        SELECT kb.SunumID, kb.BasvuruID, kb.Ogrenci1No, kb.Ogrenci2No,
               kb.OncelikSirasi, kb.ZamanDamgasi,
               o1.AdSoyad AS Ad1, o2.AdSoyad AS Ad2
        FROM KonuBasvurulari kb
        LEFT JOIN Ogrenciler o1 ON o1.OgrenciNo = kb.Ogrenci1No
        LEFT JOIN Ogrenciler o2 ON o2.OgrenciNo = kb.Ogrenci2No
        WHERE kb.SunumID = ANY(%s)
        ORDER BY kb.OncelikSirasi
    """, (slot_ids,))
    basvurular_map = {}
    for row in cursor.fetchall():
        basvurular_map.setdefault(row.SunumID, []).append(row)

    # Soru sayıları — toplam + sunum sahibi onaylı + kontrolcü onaylı + tam onaylı
    cursor.execute("""
        SELECT SunumID,
               COUNT(*) AS toplam,
               COUNT(*) FILTER (WHERE SunanOnayi = TRUE) AS sunan_onayli,
               COUNT(*) FILTER (WHERE IsApproved = TRUE) AS hakem_onayli,
               COUNT(*) FILTER (WHERE IsApproved = TRUE AND SunanOnayi = TRUE) AS tam_onayli
        FROM SoruBasvurulari
        WHERE SunumID = ANY(%s)
        GROUP BY SunumID
    """, (slot_ids,))
    soru_map = {}
    for row in cursor.fetchall():
        soru_map[row.SunumID] = {
            'toplam': row.toplam,
            'sunan_onayli': row.sunan_onayli,
            'hakem_onayli': row.hakem_onayli,
            'tam_onayli': row.tam_onayli,
        }

    # Yüklenen dosyalar (sunum/demo/kaynak)
    cursor.execute("""
        SELECT d.SunumID, d.DosyaID, d.DosyaTipi, d.DosyaAdi, d.DosyaBoyutu,
               d.YuklemeTarihi, d.Aciklama,
               o.OgrenciNo AS YukleyenNo, o.AdSoyad AS YukleyenAd
        FROM SunumDosyalari d
        LEFT JOIN Ogrenciler o ON o.OgrenciID = d.YukleyenOgrenciID
        WHERE d.SunumID = ANY(%s)
        ORDER BY d.SunumID, d.YuklemeTarihi DESC
    """, (slot_ids,))
    dosya_map = {}
    for row in cursor.fetchall():
        dosya_map.setdefault(row.SunumID, []).append(row)

    # Birleştir
    schedule_data = []
    for s in slots:
        atananlar = atananlar_map.get(s.SunumID, [])
        onaylanan_nolar = set(a.OgrenciNo for a in atananlar)
        basvurular_raw = basvurular_map.get(s.SunumID, [])

        onaylanan_basvuru_id = _find_approved_basvuru(basvurular_raw, onaylanan_nolar)

        basvurular = []
        for b in basvurular_raw:
            ogr1_label = b.Ogrenci1No + (f"({b.Ad1})" if b.Ad1 else "")
            ogr2_label = None
            if b.Ogrenci2No and b.Ogrenci2No != '0':
                ogr2_label = b.Ogrenci2No + (f"({b.Ad2})" if b.Ad2 else "")
            basvurular.append({
                'BasvuruID': b.BasvuruID,
                'Ogrenci1No': b.Ogrenci1No,
                'Ogrenci2No': b.Ogrenci2No,
                'Ogr1Label': ogr1_label,
                'Ogr2Label': ogr2_label,
                'OncelikSirasi': b.OncelikSirasi,
                'ZamanDamgasi': b.ZamanDamgasi,
                'IsApproved': (b.BasvuruID == onaylanan_basvuru_id)
            })
        basvurular.sort(key=lambda x: (0 if x['IsApproved'] else 1, x['OncelikSirasi']))

        schedule_data.append({
            'SunumID': s.SunumID,
            'HaftaNo': s.HaftaNo,
            'KonuAdi': s.KonuAdi,
            'SunumTarihi': s.SunumTarihi,
            'Basvurular': basvurular,
            'Atananlar': atananlar,
            'Onaylanan': len(atananlar) > 0,
            'OnaylananBasvuruID': onaylanan_basvuru_id,
            'SoruSayisi': soru_map.get(s.SunumID, {}).get('toplam', 0),
            'SoruOzet': soru_map.get(s.SunumID, {'toplam': 0, 'sunan_onayli': 0, 'hakem_onayli': 0, 'tam_onayli': 0}),
            'Dosyalar': dosya_map.get(s.SunumID, []),
        })

    return schedule_data


def _find_approved_basvuru(basvurular_raw, onaylanan_nolar):
    """Onaylanan başvuru ID'sini bulur."""
    if not onaylanan_nolar:
        return None

    for b in basvurular_raw:
        app_students = set(no for no in [b.Ogrenci1No, b.Ogrenci2No] if no and no != '0')
        if app_students == set(onaylanan_nolar):
            return b.BasvuruID

    for b in basvurular_raw:
        if (b.Ogrenci1No in onaylanan_nolar) or (b.Ogrenci2No and b.Ogrenci2No in onaylanan_nolar):
            return b.BasvuruID

    return None


# ===========================================================================
# Vize / Tatil çoklu-bölüm senkronizasyon yardımcıları
# ===========================================================================

def _get_donem_id(cursor, bolum_id):
    cursor.execute("SELECT donemid FROM Bolumler WHERE bolumid = %s", (bolum_id,))
    r = cursor.fetchone()
    return r.donemid if r else None


def get_donem_bolum_ids(cursor, source_bolum_id, restrict_bolum_ids=None, include_source=False):
    """Aynı dönemdeki bölüm ID'lerini döndürür.
    restrict_bolum_ids verilirse (admin için) sadece o set ile kesişim alınır.
    """
    donem_id = _get_donem_id(cursor, source_bolum_id)
    if donem_id is None:
        return []
    params = [donem_id]
    sql = "SELECT bolumid FROM Bolumler WHERE donemid = %s"
    if not include_source:
        sql += " AND bolumid <> %s"
        params.append(source_bolum_id)
    if restrict_bolum_ids is not None:
        sql += " AND bolumid = ANY(%s)"
        params.append(list(restrict_bolum_ids))
    cursor.execute(sql, tuple(params))
    return [r.bolumid for r in cursor.fetchall()]


def resolve_hafta_tarihi(cursor, bolum_id, hafta_no, hafta_tarihi_str=None):
    """Form girdisi veya DB'den hafta tarihini çözer (date veya None)."""
    from datetime import datetime as _dt
    if hafta_tarihi_str:
        try:
            return _dt.strptime(hafta_tarihi_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    cursor.execute(
        "SELECT sunumtarihi FROM SunumProgrami "
        "WHERE bolumid=%s AND haftano=%s AND sunumtarihi IS NOT NULL LIMIT 1",
        (bolum_id, hafta_no)
    )
    r = cursor.fetchone()
    if r and r.sunumtarihi:
        return r.sunumtarihi
    cursor.execute(
        "SELECT hafta_tarihi FROM VizeHaftalari WHERE bolumid=%s AND haftano=%s",
        (bolum_id, hafta_no)
    )
    r = cursor.fetchone()
    if r and r.hafta_tarihi:
        return r.hafta_tarihi
    cursor.execute(
        "SELECT hafta_tarihi FROM TatilKaydirmaHaftalari WHERE bolumid=%s AND haftano=%s",
        (bolum_id, hafta_no)
    )
    r = cursor.fetchone()
    return r.hafta_tarihi if r and r.hafta_tarihi else None


def shift_bolum_forward(cursor, bolum_id, from_haftano):
    """Tek bölümün haftano>=N olan slotlarını ve metadata kayıtlarını +1 hafta ileri kaydır."""
    cursor.execute("""
        UPDATE SunumProgrami
        SET haftano = haftano + 1,
            sunumtarihi = CASE WHEN sunumtarihi IS NOT NULL
                               THEN sunumtarihi + make_interval(days => 7)
                               ELSE NULL END
        WHERE bolumid = %s AND haftano >= %s
    """, (bolum_id, from_haftano))
    cursor.execute(
        "UPDATE VizeHaftalari SET haftano = haftano + 1 "
        "WHERE bolumid=%s AND haftano >= %s",
        (bolum_id, from_haftano)
    )
    cursor.execute(
        "UPDATE TatilKaydirmaHaftalari SET haftano = haftano + 1 "
        "WHERE bolumid=%s AND haftano >= %s",
        (bolum_id, from_haftano)
    )


def shift_bolum_backward(cursor, bolum_id, after_haftano):
    """Tek bölümün haftano>N olan slotlarını ve metadata kayıtlarını -1 hafta geri kaydır."""
    cursor.execute("""
        UPDATE SunumProgrami
        SET haftano = haftano - 1,
            sunumtarihi = CASE WHEN sunumtarihi IS NOT NULL
                               THEN sunumtarihi - make_interval(days => 7)
                               ELSE NULL END
        WHERE bolumid = %s AND haftano > %s
    """, (bolum_id, after_haftano))
    cursor.execute(
        "UPDATE VizeHaftalari SET haftano = haftano - 1 "
        "WHERE bolumid=%s AND haftano > %s",
        (bolum_id, after_haftano)
    )
    cursor.execute(
        "UPDATE TatilKaydirmaHaftalari SET haftano = haftano - 1 "
        "WHERE bolumid=%s AND haftano > %s",
        (bolum_id, after_haftano)
    )


def _week_bounds(d):
    """Verilen tarihin Pazartesi ve Pazar gününü döndür."""
    from datetime import timedelta as _td
    monday = d - _td(days=d.weekday())
    sunday = monday + _td(days=6)
    return monday, sunday


def cross_bolum_vize_apply(cursor, bolum_ids, week_date, aciklama, islemyapan):
    """Verilen bölümlerin her birinde, week_date'in bulunduğu hafta (Pzt-Paz) içinde
    sunumu olan slotlardan en küçük haftano'yu bulup +1 hafta ileri kaydırır ve
    VizeHaftalari kaydı ekler. Geri tüm uygulanan (bolum_id, haftano) listesi.
    """
    monday, sunday = _week_bounds(week_date)
    applied = []
    for bid in bolum_ids:
        cursor.execute(
            "SELECT MIN(haftano) AS h FROM SunumProgrami "
            "WHERE bolumid=%s AND sunumtarihi IS NOT NULL "
            "AND sunumtarihi BETWEEN %s AND %s",
            (bid, monday, sunday)
        )
        r = cursor.fetchone()
        if not r or r.h is None:
            continue
        nb = r.h
        shift_bolum_forward(cursor, bid, nb)
        cursor.execute(
            "INSERT INTO VizeHaftalari (bolumid, haftano, aciklama, islemyapan, hafta_tarihi) "
            "VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            (bid, nb, aciklama, islemyapan, week_date)
        )
        applied.append((bid, nb))
    return applied


def cross_bolum_tatil_apply(cursor, bolum_ids, holiday_date, aciklama, islemyapan):
    """Verilen bölümlerin her birinde, holiday_date'in bulunduğu hafta (Pzt-Paz) içinde
    sunumu olan slotlardan en küçük haftano'yu bulup +1 hafta ileri kaydırır ve
    TatilKaydirmaHaftalari kaydı ekler. Tatil günü hangi gün olursa olsun o haftanın
    tamamı bir sonraki haftaya öteler (hafta tatil olarak işaretlenmiş sayılır).
    """
    monday, sunday = _week_bounds(holiday_date)
    applied = []
    for bid in bolum_ids:
        cursor.execute(
            "SELECT MIN(haftano) AS h FROM SunumProgrami "
            "WHERE bolumid=%s AND sunumtarihi IS NOT NULL "
            "AND sunumtarihi BETWEEN %s AND %s",
            (bid, monday, sunday)
        )
        r = cursor.fetchone()
        if not r or r.h is None:
            continue
        nb = r.h
        shift_bolum_forward(cursor, bid, nb)
        cursor.execute(
            "INSERT INTO TatilKaydirmaHaftalari (bolumid, haftano, aciklama, islemyapan, hafta_tarihi) "
            "VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            (bid, nb, aciklama, islemyapan, holiday_date)
        )
        applied.append((bid, nb))
    return applied


def cross_bolum_vize_remove(cursor, bolum_ids, hafta_tarihi):
    """hafta_tarihi eşleşen tüm VizeHaftalari kayıtlarını sil ve ilgili bölümleri geri kaydır."""
    if not bolum_ids or not hafta_tarihi:
        return []
    cursor.execute(
        "SELECT vizeid, bolumid, haftano FROM VizeHaftalari "
        "WHERE bolumid = ANY(%s) AND hafta_tarihi = %s "
        "ORDER BY haftano DESC",
        (list(bolum_ids), hafta_tarihi)
    )
    rows = cursor.fetchall()
    out = []
    for r in rows:
        cursor.execute("DELETE FROM VizeHaftalari WHERE vizeid=%s", (r.vizeid,))
        shift_bolum_backward(cursor, r.bolumid, r.haftano)
        out.append((r.bolumid, r.haftano))
    return out


def cross_bolum_tatil_remove(cursor, bolum_ids, hafta_tarihi):
    """hafta_tarihi eşleşen tüm TatilKaydirmaHaftalari kayıtlarını sil ve geri kaydır."""
    if not bolum_ids or not hafta_tarihi:
        return []
    cursor.execute(
        "SELECT tatilkaydiraid, bolumid, haftano FROM TatilKaydirmaHaftalari "
        "WHERE bolumid = ANY(%s) AND hafta_tarihi = %s "
        "ORDER BY haftano DESC",
        (list(bolum_ids), hafta_tarihi)
    )
    rows = cursor.fetchall()
    out = []
    for r in rows:
        cursor.execute("DELETE FROM TatilKaydirmaHaftalari WHERE tatilkaydiraid=%s", (r.tatilkaydiraid,))
        shift_bolum_backward(cursor, r.bolumid, r.haftano)
        out.append((r.bolumid, r.haftano))
    return out


# ===========================================================================
# Otomatik Yerleştirme (Sarkık konuları takvime sığdırma)
# ===========================================================================

def auto_fit_apply(cursor, bolum_id, islemyapan):
    """Akademik takvim bitişini aşan slotları, mevcut konu sırasını koruyarak
    erken haftalara yeniden dağıtır (yukarıya doğru domino kaydırma).

    Geçmiş haftalardaki slotlara dokunulmaz. Mevcut sıraya göre yeni
    haftano/sunumtarihi atanır; her hafta için yoğunluk = ceil(N / W).

    Returns (gecmisid, info_dict) — başarısızsa (None, {'error': ...}).
    """
    from datetime import date as _date, timedelta as _td
    import json
    import math

    cursor.execute("""
        SELECT d.donembitis FROM Donemler d
        JOIN Bolumler b ON b.donemid = d.donemid
        WHERE b.bolumid = %s
    """, (bolum_id,))
    r = cursor.fetchone()
    if not r or not r.donembitis:
        return None, {'error': 'Akademik takvim bitiş tarihi tanımlı değil.'}
    end_date = r.donembitis
    today = _date.today()

    cursor.execute("""
        SELECT sp.SunumID, sp.HaftaNo, sp.SunumTarihi, k.SiraNo
        FROM SunumProgrami sp JOIN Konular k ON sp.KonuID = k.KonuID
        WHERE sp.BolumID = %s
        ORDER BY sp.HaftaNo, k.SiraNo, sp.SunumID
    """, (bolum_id,))
    all_slots = cursor.fetchall()
    if not all_slots:
        return None, {'error': 'Slot bulunamadı.'}

    # Geçmiş slotlara (sunum_tarihi < bugün) dokunma
    movable_start_idx = len(all_slots)
    for i, s in enumerate(all_slots):
        if not s.SunumTarihi or s.SunumTarihi >= today:
            movable_start_idx = i
            break
    immutable = list(all_slots[:movable_start_idx])
    movable = list(all_slots[movable_start_idx:])
    if not movable:
        return None, {'error': 'Taşınacak slot yok (tüm slotlar geçmişte).'}

    overflow_count = sum(1 for s in movable if s.SunumTarihi and s.SunumTarihi > end_date)
    if overflow_count == 0:
        return None, {'error': 'Akademik takvimi aşan slot yok.'}

    # Başlangıç haftası ve tarihi
    if movable[0].SunumTarihi:
        start_date = movable[0].SunumTarihi
        start_haftano = movable[0].HaftaNo
    elif immutable and immutable[-1].SunumTarihi:
        start_date = immutable[-1].SunumTarihi + _td(days=7)
        start_haftano = immutable[-1].HaftaNo + 1
    else:
        return None, {'error': 'Başlangıç haftası belirlenemedi.'}

    if start_date > end_date:
        return None, {'error': 'Başlangıç tarihi akademik takvim bitişinden sonra; otomatik yerleştirme yapılamaz.'}

    # Tatil/Vize haftalarını topla — bu haftalara konu yerleştirilmeyecek.
    cursor.execute(
        "SELECT haftano FROM VizeHaftalari WHERE bolumid=%s "
        "UNION SELECT haftano FROM TatilKaydirmaHaftalari WHERE bolumid=%s",
        (bolum_id, bolum_id)
    )
    blocked = {r.haftano for r in cursor.fetchall()}

    # Başlangıçtan akademik takvim bitişine kadar uygun (engelsiz) haftaları sırala.
    available = []  # list of (haftano, date)
    cur_h = start_haftano
    cur_d = start_date
    while cur_d <= end_date:
        if cur_h not in blocked:
            available.append((cur_h, cur_d))
        cur_h += 1
        cur_d = cur_d + _td(days=7)

    if not available:
        return None, {'error': 'Akademik takvimde uygun (tatil/vize dışı) hafta yok.'}

    weeks_W = len(available)
    N = len(movable)
    # Dengeli dağıtım: önce her haftaya base = N // W konu, sonra ilk `extra` haftaya +1.
    # Örn N=13, W=5 -> [3,3,3,2,2] (8-8-8-4 yerine).
    base = N // weeks_W
    extra = N % weeks_W
    per_week = [base + (1 if w < extra else 0) for w in range(weeks_W)]

    # Snapshot
    snapshot = [
        {
            'sid': s.SunumID,
            'h': s.HaftaNo,
            'd': s.SunumTarihi.isoformat() if s.SunumTarihi else None,
        }
        for s in movable
    ]

    # Yeniden ata — sırayı koruyarak haftaları doldur (engellenmiş haftaları atlayarak)
    idx = 0
    cursor_pos = 0
    for week_i, count in enumerate(per_week):
        new_haftano, new_date = available[week_i]
        for _ in range(count):
            s = movable[cursor_pos]
            cursor.execute(
                "UPDATE SunumProgrami SET HaftaNo=%s, SunumTarihi=%s WHERE SunumID=%s",
                (new_haftano, new_date, s.SunumID)
            )
            cursor_pos += 1

    cursor.execute(
        "INSERT INTO OtomatikYerlesimGecmisi (bolumid, snapshot, islemyapan) "
        "VALUES (%s, %s::jsonb, %s) RETURNING gecmisid",
        (bolum_id, json.dumps(snapshot), islemyapan)
    )
    gid = cursor.fetchone().gecmisid
    return gid, {
        'overflow_count': overflow_count,
        'moved_count': len(movable),
        'min_per_week': base,
        'max_per_week': base + (1 if extra else 0),
        'weeks_used': weeks_W,
        'blocked_weeks': len(blocked),
    }


def auto_fit_undo(cursor, gecmisid, bolum_id):
    """Snapshot'tan slot pozisyonlarını geri yükle. Returns True/False."""
    import json
    cursor.execute(
        "SELECT snapshot, bolumid FROM OtomatikYerlesimGecmisi "
        "WHERE gecmisid=%s AND geri_alindi=false",
        (gecmisid,)
    )
    r = cursor.fetchone()
    if not r:
        return False
    if str(r.bolumid) != str(bolum_id):
        return False
    snap = r.snapshot if isinstance(r.snapshot, (list, dict)) else json.loads(r.snapshot)
    for item in snap:
        d = item.get('d')
        cursor.execute(
            "UPDATE SunumProgrami SET HaftaNo=%s, SunumTarihi=%s WHERE SunumID=%s",
            (item['h'], d, item['sid'])
        )
    cursor.execute(
        "UPDATE OtomatikYerlesimGecmisi SET geri_alindi=true WHERE gecmisid=%s",
        (gecmisid,)
    )
    return True


def auto_fit_active_snapshot(cursor, bolum_id):
    """Bölüm için en son geri alınmamış snapshot kaydını döndür (yoksa None)."""
    cursor.execute(
        "SELECT gecmisid, olusturma_tarihi, islemyapan FROM OtomatikYerlesimGecmisi "
        "WHERE bolumid=%s AND geri_alindi=false "
        "ORDER BY gecmisid DESC LIMIT 1",
        (bolum_id,)
    )
    return cursor.fetchone()


