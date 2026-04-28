from app import create_app
app = create_app()
with app.test_request_context():
    from db_manager import get_db_connection, init_pool
    init_pool()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM TatilGunleri")
        print("TatilGunleri OK, count:", cursor.fetchone()[0])
    except Exception as e:
        print("TatilGunleri HATA:", type(e).__name__, str(e))
    try:
        cursor.execute("SELECT COUNT(*) FROM Admins WHERE IsApproved=TRUE")
        print("Admins OK, count:", cursor.fetchone()[0])
    except Exception as e:
        print("Admins HATA:", type(e).__name__, str(e))
    try:
        cursor.execute("SELECT COUNT(*) FROM Hocalar WHERE IsApproved=TRUE")
        print("Hocalar OK, count:", cursor.fetchone()[0])
    except Exception as e:
        print("Hocalar HATA:", type(e).__name__, str(e))
