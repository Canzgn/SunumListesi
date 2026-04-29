-- 004: TatilKaydirmaHaftalari tablosu
-- Bir hafta "Bu haftadan itibaren kaydır" ile kaydırıldığında kayıt tutulur.
-- VizeHaftalari ile paralel yapı; sadece gösterim/kayıt amaçlıdır, shift kalıcıdır.

CREATE TABLE IF NOT EXISTS public.tatilkaydirmahaftalari (
    tatilkaydiraid  serial      PRIMARY KEY,
    bolumid         integer     NOT NULL REFERENCES public.bolumler(bolumid) ON DELETE CASCADE,
    haftano         integer     NOT NULL,
    UNIQUE (bolumid, haftano)
);
