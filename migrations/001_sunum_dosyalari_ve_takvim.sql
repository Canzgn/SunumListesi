-- =====================================================================
-- Migration 001: Sunum Dosyaları, Soru İçeriği/Çift Onay, Akademik Takvim
-- Branch: feat/sunum-dosya-yukleme (+ takvim/tatil için temel kolonlar)
-- Tarih: 2026-04-28
--
-- NOT: PostgreSQL tırnaksız tanımlayıcıları lowercase'e çevirir. Mevcut
-- şema lowercase olduğu için (donemler, sorubasvurulari ...) burada da
-- lowercase + IF NOT EXISTS ile yazıyoruz. Tek seferde çalıştırın.
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 1) Sunum Dosyaları (sunum / demo / kaynak)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.sunumdosyalari (
    dosyaid            serial PRIMARY KEY,
    sunumid            integer NOT NULL REFERENCES public.sunumprogrami(sunumid) ON DELETE CASCADE,
    yukleyenogrenciid  integer REFERENCES public.ogrenciler(ogrenciid) ON DELETE SET NULL,
    dosyatipi          varchar(20) NOT NULL CHECK (dosyatipi IN ('sunum','demo','kaynak')),
    dosyaadi           varchar(255) NOT NULL,
    dosyayolu          varchar(500) NOT NULL,   -- Supabase Storage path veya public URL
    dosyaboyutu        integer,
    yuklemetarihi      timestamp DEFAULT now(),
    aciklama           text
);

CREATE INDEX IF NOT EXISTS idx_sunumdosyalari_sunumid ON public.sunumdosyalari(sunumid);
CREATE INDEX IF NOT EXISTS idx_sunumdosyalari_tip    ON public.sunumdosyalari(sunumid, dosyatipi);

-- ---------------------------------------------------------------------
-- 2) SoruBasvurulari: soru metni + çift onay (sunan + kontrolcü)
-- ---------------------------------------------------------------------
ALTER TABLE public.sorubasvurulari ADD COLUMN IF NOT EXISTS soruicerigi      text;
ALTER TABLE public.sorubasvurulari ADD COLUMN IF NOT EXISTS sunanonayi       boolean DEFAULT NULL;  -- NULL=bekliyor, T=onay, F=red
ALTER TABLE public.sorubasvurulari ADD COLUMN IF NOT EXISTS sunanonaytarihi  timestamp;
ALTER TABLE public.sorubasvurulari ADD COLUMN IF NOT EXISTS sunanredsebep    varchar(255);

-- ---------------------------------------------------------------------
-- 3) Akademik Takvim — Donemler tablosuna başlangıç/bitiş
-- ---------------------------------------------------------------------
ALTER TABLE public.donemler ADD COLUMN IF NOT EXISTS donembaslangic date;
ALTER TABLE public.donemler ADD COLUMN IF NOT EXISTS donembitis     date;

-- ---------------------------------------------------------------------
-- 4) Tatil Günleri (1 Mayıs vb.)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.tatilgunleri (
    tatilid     serial PRIMARY KEY,
    donemid     integer NOT NULL REFERENCES public.donemler(donemid) ON DELETE CASCADE,
    tarih       date NOT NULL,
    aciklama    varchar(255),
    eylemtipi   varchar(20) NOT NULL DEFAULT 'kaydir'
                CHECK (eylemtipi IN ('kaydir','iptal','bilgi')),
    UNIQUE (donemid, tarih)
);

CREATE INDEX IF NOT EXISTS idx_tatilgunleri_donem ON public.tatilgunleri(donemid, tarih);

COMMIT;

-- =====================================================================
-- (Opsiyonel) Seed: 2026 Bahar dönemi resmi tatilleri
-- Aktif dönemin DonemID'sini öğrenip aşağıdakini ayrıca çalıştırabilirsiniz.
-- =====================================================================
-- INSERT INTO public.tatilgunleri (donemid, tarih, aciklama, eylemtipi) VALUES
--   ((SELECT donemid FROM public.donemler WHERE aktif = TRUE LIMIT 1), '2026-05-01', '1 Mayıs Emek ve Dayanışma Günü', 'kaydir'),
--   ((SELECT donemid FROM public.donemler WHERE aktif = TRUE LIMIT 1), '2026-05-19', '19 Mayıs Atatürk''ü Anma Genç. ve Spor B.', 'kaydir')
-- ON CONFLICT (donemid, tarih) DO NOTHING;
