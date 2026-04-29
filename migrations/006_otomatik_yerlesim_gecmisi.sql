-- 006: OtomatikYerlesimGecmisi tablosu
-- "Konular takvime sığmıyor" durumunda kullanıcı 'Otomatik Yerleştir' butonuna basarsa
-- mevcut slotların haftano + sunumtarihi snapshot'ı bu tabloya kaydedilir.
-- Geri alma yalnızca son uygulanan (en yeni) snapshot için anlamlıdır.

CREATE TABLE IF NOT EXISTS public.otomatikyerlesimgecmisi (
    gecmisid          serial      PRIMARY KEY,
    bolumid           integer     NOT NULL REFERENCES public.bolumler(bolumid) ON DELETE CASCADE,
    snapshot          jsonb       NOT NULL,
    islemyapan        varchar(150),
    olusturma_tarihi  timestamptz DEFAULT now(),
    geri_alindi       boolean     DEFAULT false
);

CREATE INDEX IF NOT EXISTS idx_oyg_bolum_aktif
    ON public.otomatikyerlesimgecmisi(bolumid)
    WHERE geri_alindi = false;
