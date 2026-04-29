-- 005: VizeHaftalari ve TatilKaydirmaHaftalari tablolarına metadata kolonları eklendi
-- aciklama: işaretlenme sebebi (örn. "1 Mayıs İşçi Bayramı")
-- islemyapan: işlemi yapan kişinin adı
-- hafta_tarihi: o haftanın tarihi (sunum_tarihi ile senkronize, boş olabilir)
-- olusturma_tarihi: kaydın oluşturulma zamanı

ALTER TABLE public.vizehaftalari
    ADD COLUMN IF NOT EXISTS islemyapan   varchar(150),
    ADD COLUMN IF NOT EXISTS hafta_tarihi date,
    ADD COLUMN IF NOT EXISTS olusturma_tarihi timestamptz DEFAULT now();

ALTER TABLE public.tatilkaydirmahaftalari
    ADD COLUMN IF NOT EXISTS aciklama     varchar(255),
    ADD COLUMN IF NOT EXISTS islemyapan   varchar(150),
    ADD COLUMN IF NOT EXISTS hafta_tarihi date,
    ADD COLUMN IF NOT EXISTS olusturma_tarihi timestamptz DEFAULT now();
