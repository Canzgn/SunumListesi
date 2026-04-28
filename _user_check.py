from app import create_app
app = create_app()

with app.test_request_context():
    from db_manager import get_db_connection, init_pool
    init_pool()
    conn = get_db_connection()
    cursor = conn.cursor()

    print("=== ADMINS ===")
    cursor.execute("SELECT AdminID, Username, AdSoyad, IsApproved, Password FROM Admins")
    for r in cursor.fetchall():
        pw_preview = r.password[:40] + "..." if r.password and len(r.password) > 40 else r.password
        print(f"  ID={r.adminid} | User={r.username} | Onaylı={r.isapproved} | Hash={pw_preview}")

    print("\n=== HOCALAR ===")
    cursor.execute("SELECT HocaID, Username, AdSoyad, IsApproved, Password FROM Hocalar")
    for r in cursor.fetchall():
        pw_preview = r.password[:40] + "..." if r.password and len(r.password) > 40 else r.password
        print(f"  ID={r.hocaid} | User={r.username} | Onaylı={r.isapproved} | Hash={pw_preview}")
