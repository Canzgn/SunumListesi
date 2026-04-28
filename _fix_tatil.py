"""Kurban Bayramı tatil kayıtlarını 27-30 Mayıs 2026 olarak günceller."""
from app import create_app
app = create_app()

with app.test_request_context():
    from db_manager import get_db_connection, init_pool
    init_pool()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Mevcut Kurban Bayramı kayıtlarını sil
    cursor.execute("""
        DELETE FROM TatilGunleri 
        WHERE donemid=1 AND aciklama ILIKE 'Kurban%'
    """)
    deleted = cursor.rowcount
    print(f"Silinen Kurban kayıtları: {deleted}")

    # Doğru tarihlerle yeniden ekle
    tatiller = [
        ('2026-05-27', 'Kurban Bayramı (1. Gün)', 'kaydir'),
        ('2026-05-28', 'Kurban Bayramı (2. Gün)', 'bilgi'),
        ('2026-05-29', 'Kurban Bayramı (3. Gün)', 'bilgi'),
        ('2026-05-30', 'Kurban Bayramı (4. Gün)', 'bilgi'),
    ]
    for tarih, aciklama, eylem in tatiller:
        cursor.execute("""
            INSERT INTO TatilGunleri (donemid, tarih, aciklama, eylemtipi)
            VALUES (1, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (tarih, aciklama, eylem))
        print(f"  Eklendi: {tarih} | {aciklama} | {eylem}")

    conn.commit()
    print("\nGüncel TatilGunleri (donemid=1):")
    cursor.execute("SELECT tarih, aciklama, eylemtipi FROM TatilGunleri WHERE donemid=1 ORDER BY tarih")
    for r in cursor.fetchall():
        print(f"  {r.tarih} | {r.aciklama} | {r.eylemtipi}")
