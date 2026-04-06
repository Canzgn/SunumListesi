-- Supabase SQL Editor'de bu dosyayı çalıştır

CREATE TABLE IF NOT EXISTS Konular (
    KonuID SERIAL PRIMARY KEY,
    KonuAdi VARCHAR(255) NOT NULL,
    SiraNo INT NOT NULL
);

CREATE TABLE IF NOT EXISTS SunumProgrami (
    SunumID SERIAL PRIMARY KEY,
    KonuID INT REFERENCES Konular(KonuID),
    OgretimTuru VARCHAR(20) NOT NULL,
    HaftaNo INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Admins (
    AdminID SERIAL PRIMARY KEY,
    Username VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    AdSoyad VARCHAR(255),
    IsApproved BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Ogrenciler (
    OgrenciID SERIAL PRIMARY KEY,
    OgrenciNo VARCHAR(50) UNIQUE NOT NULL,
    AdSoyad VARCHAR(255),
    OgretimTuru VARCHAR(20),
    IsApproved BOOLEAN DEFAULT FALSE,
    KimlikFoto VARCHAR(255),
    KayitTarihi TIMESTAMP,
    Password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS KonuBasvurulari (
    BasvuruID SERIAL PRIMARY KEY,
    SunumID INT REFERENCES SunumProgrami(SunumID),
    Ogrenci1No VARCHAR(50),
    Ogrenci2No VARCHAR(50) DEFAULT '0',
    OncelikSirasi INT,
    ZamanDamgasi TIMESTAMP
);

CREATE TABLE IF NOT EXISTS SunumGorevlileri (
    GorevID SERIAL PRIMARY KEY,
    SunumID INT REFERENCES SunumProgrami(SunumID),
    OgrenciID INT REFERENCES Ogrenciler(OgrenciID)
);

CREATE TABLE IF NOT EXISTS SoruBasvurulari (
    SoruBasvuruID SERIAL PRIMARY KEY,
    SunumID INT REFERENCES SunumProgrami(SunumID),
    OgrenciNo VARCHAR(50),
    ZamanDamgasi TIMESTAMP,
    IsApproved BOOLEAN DEFAULT TRUE,
    RejectReason VARCHAR(255)
);

-- RLS: Supabase Data API icin tanimlanmisti.
-- Docker / dogrudan baglantida superuser RLS'yi bypass eder,
-- ancak politikalar olusturulurken CURRENT_USER kullanilir.
ALTER TABLE Konular ENABLE ROW LEVEL SECURITY;
ALTER TABLE SunumProgrami ENABLE ROW LEVEL SECURITY;
ALTER TABLE Admins ENABLE ROW LEVEL SECURITY;
ALTER TABLE Ogrenciler ENABLE ROW LEVEL SECURITY;
ALTER TABLE KonuBasvurulari ENABLE ROW LEVEL SECURITY;
ALTER TABLE SunumGorevlileri ENABLE ROW LEVEL SECURITY;
ALTER TABLE SoruBasvurulari ENABLE ROW LEVEL SECURITY;

CREATE POLICY "backend_full_access" ON Konular FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON SunumProgrami FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON Admins FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON Ogrenciler FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON KonuBasvurulari FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON SunumGorevlileri FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON SoruBasvurulari FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);

-- ─── YENİ TABLOLAR (Faz 1 - 4) ───────────────────────────────────────────────

-- Akademik dönemler
CREATE TABLE IF NOT EXISTS Donemler (
    DonemID SERIAL PRIMARY KEY,
    DonemAdi VARCHAR(20) NOT NULL UNIQUE,  -- "2025/26"
    Aktif BOOLEAN DEFAULT FALSE,
    BasvuruBitis TIMESTAMP
);

-- Bölümler / dersler (bir öğretmenin verebileceği her ders kümesi)
CREATE TABLE IF NOT EXISTS Bolumler (
    BolumID SERIAL PRIMARY KEY,
    BolumAdi VARCHAR(100) NOT NULL,
    OgretimTuru VARCHAR(20) NOT NULL,      -- Örgün / Gece
    DonemID INT REFERENCES Donemler(DonemID) ON DELETE CASCADE,
    UNIQUE (BolumAdi, OgretimTuru, DonemID)
);

-- Öğretmenler
CREATE TABLE IF NOT EXISTS Hocalar (
    HocaID SERIAL PRIMARY KEY,
    Username VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    AdSoyad VARCHAR(255),
    IsApproved BOOLEAN DEFAULT FALSE
);

-- Öğretmen ↔ Bölüm ilişkisi (bir öğretmen birden fazla bölüm verebilir)
CREATE TABLE IF NOT EXISTS HocaBolumler (
    HocaID INT REFERENCES Hocalar(HocaID) ON DELETE CASCADE,
    BolumID INT REFERENCES Bolumler(BolumID) ON DELETE CASCADE,
    PRIMARY KEY (HocaID, BolumID)
);

-- Admin ↔ Bölüm ilişkisi
CREATE TABLE IF NOT EXISTS AdminBolumler (
    AdminID INT REFERENCES Admins(AdminID) ON DELETE CASCADE,
    BolumID INT REFERENCES Bolumler(BolumID) ON DELETE CASCADE,
    PRIMARY KEY (AdminID, BolumID)
);

-- Duyurular
CREATE TABLE IF NOT EXISTS Duyurular (
    DuyuruID SERIAL PRIMARY KEY,
    Baslik VARCHAR(255) NOT NULL,
    Icerik TEXT,
    YayinlayaciAdi VARCHAR(255),
    GosterilecekRoller VARCHAR(50) DEFAULT 'all',
    OlusturmaTarihi TIMESTAMP DEFAULT NOW()
);

-- İşlem logları
CREATE TABLE IF NOT EXISTS IslemLoglari (
    LogID SERIAL PRIMARY KEY,
    Eylem VARCHAR(50),
    SunumID INT,
    KonuAdi VARCHAR(255),
    YapaAdi VARCHAR(255),
    Detay TEXT,
    ZamanDamgasi TIMESTAMP DEFAULT NOW()
);

-- Soru Kontrolcüleri
CREATE TABLE IF NOT EXISTS SoruKontrolculeri (
    KontrolcuID SERIAL PRIMARY KEY,
    Username VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    AdSoyad VARCHAR(255),
    IsApproved BOOLEAN DEFAULT FALSE,
    BolumID INT REFERENCES Bolumler(BolumID) ON DELETE SET NULL
);

-- ─── MEVCUT TABLOLARA KOLON EKLEMELERİ ──────────────────────────────────────
-- (IF NOT EXISTS eşdeğeri: hata fırlatmadan çalışır)
ALTER TABLE Ogrenciler ADD COLUMN IF NOT EXISTS BolumID INT REFERENCES Bolumler(BolumID) ON DELETE SET NULL;
ALTER TABLE Ogrenciler ADD COLUMN IF NOT EXISTS DonemID INT REFERENCES Donemler(DonemID) ON DELETE SET NULL;
ALTER TABLE SunumProgrami ADD COLUMN IF NOT EXISTS BolumID INT REFERENCES Bolumler(BolumID) ON DELETE SET NULL;
ALTER TABLE Admins ADD COLUMN IF NOT EXISTS BolumID INT REFERENCES Bolumler(BolumID) ON DELETE SET NULL;
ALTER TABLE SunumProgrami ADD COLUMN IF NOT EXISTS SunumTarihi DATE;

-- Yeni tablolar icin RLS
ALTER TABLE AdminBolumler ENABLE ROW LEVEL SECURITY;
ALTER TABLE Duyurular ENABLE ROW LEVEL SECURITY;
ALTER TABLE IslemLoglari ENABLE ROW LEVEL SECURITY;
CREATE POLICY "backend_full_access" ON AdminBolumler FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON Duyurular FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON IslemLoglari FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);

-- ─── RLS ─────────────────────────────────────────────────────────────────────
ALTER TABLE Donemler ENABLE ROW LEVEL SECURITY;
ALTER TABLE Bolumler ENABLE ROW LEVEL SECURITY;
ALTER TABLE Hocalar ENABLE ROW LEVEL SECURITY;
ALTER TABLE HocaBolumler ENABLE ROW LEVEL SECURITY;
ALTER TABLE SoruKontrolculeri ENABLE ROW LEVEL SECURITY;

CREATE POLICY "backend_full_access" ON Donemler FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON Bolumler FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON Hocalar FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON HocaBolumler FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);
CREATE POLICY "backend_full_access" ON SoruKontrolculeri FOR ALL TO CURRENT_USER USING (true) WITH CHECK (true);

-- ─── BAŞLANGIÇ VERİSİ ────────────────────────────────────────────────────────
-- Tüm veriler seed_data.sql dosyasından yüklenir (docker-entrypoint-initdb.d/02_seed_data.sql).
