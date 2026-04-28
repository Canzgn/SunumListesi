"""003_vize_haftalari.sql migration'ını çalıştırır."""
from app import create_app
app = create_app()

with app.test_request_context():
    from db_manager import get_db_connection, init_pool
    init_pool()
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = open('migrations/003_vize_haftalari.sql', encoding='utf-8').read()
    cursor.execute(sql)
    conn.commit()
    print("Migration 003 başarıyla uygulandı.")

    cursor.execute("SELECT COUNT(*) FROM VizeHaftalari")
    print("VizeHaftalari count:", cursor.fetchone()[0])
