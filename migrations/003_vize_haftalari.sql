-- 003: VizeHaftalari tablosu
-- Hoca/admin belirli bir bölüm için bir haftayı "vize haftası" olarak işaretleyebilir.
-- Bu işaret sırasında o hafta ve sonraki tüm haftalar 1 hafta ileri kaydırılır.
-- Bu tablo sadece kayıt/gösterim amaçlıdır (shift kalıcı yapılır).

CREATE TABLE IF NOT EXISTS public.vizehaftalari (
    vizeid    serial      PRIMARY KEY,
    bolumid   integer     NOT NULL REFERENCES public.bolumler(bolumid)  ON DELETE CASCADE,
    haftano   integer     NOT NULL,
    aciklama  varchar(255),
    UNIQUE (bolumid, haftano)
);
