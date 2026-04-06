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

    # Soru sayıları
    cursor.execute("""
        SELECT SunumID, COUNT(*) AS sayi
        FROM SoruBasvurulari
        WHERE SunumID = ANY(%s)
        GROUP BY SunumID
    """, (slot_ids,))
    soru_map = {row.SunumID: row.sayi for row in cursor.fetchall()}

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
            'SoruSayisi': soru_map.get(s.SunumID, 0)
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
