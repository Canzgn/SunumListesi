import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ['PYTHONIOENCODING'] = 'utf-8'
from dotenv import load_dotenv
load_dotenv()

import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ.get('DATABASE_URL', '')
conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.NamedTupleCursor)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Mesajlar (
        MesajID SERIAL PRIMARY KEY,
        GonderenRol VARCHAR(20) NOT NULL,
        GonderenID INT NOT NULL,
        GonderenAdi VARCHAR(255),
        AliciRol VARCHAR(20) NOT NULL,
        AliciID INT,
        Konu VARCHAR(255) NOT NULL,
        Icerik TEXT NOT NULL,
        Okundu BOOLEAN DEFAULT FALSE,
        GonderimTarihi TIMESTAMP DEFAULT NOW()
    )
""")
conn.commit()
conn.close()
print("Mesajlar tablosu olusturuldu.")
