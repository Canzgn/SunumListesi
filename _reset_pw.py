from app import create_app
from werkzeug.security import generate_password_hash

app = create_app()
new_pw = "admin123."
hashed = generate_password_hash(new_pw)

with app.test_request_context():
    from db_manager import get_db_connection, init_pool
    init_pool()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE Admins SET Password=%s WHERE Username IN ('admin', 'ahmet')", (hashed,))
    cursor.execute("UPDATE Hocalar SET Password=%s WHERE Username IN ('hoca1', 'uguryildiz')", (hashed,))
    conn.commit()
    print("Şifreler güncellendi.")
    print("Yeni şifre:", new_pw)
    print("Admin kullanıcıları: admin, ahmet")
    print("Hoca kullanıcıları: hoca1, uguryildiz")
