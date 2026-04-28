-- Migration 002: SoruBasvurulari.IsApproved sıfırlama
-- Amaç: Admin onaylarını NULL'a çekip yeni 2-adım onay akışını (Sunan → Admin)
--        sıfırdan test edebilmek için.
-- SADECE GELİŞTİRME / TEST ortamında çalıştırın.
-- Üretim ortamında admin ile mutabık olarak çalıştırın.

UPDATE SoruBasvurulari
SET IsApproved = NULL,
    RejectReason = NULL
WHERE IsApproved IS NOT NULL;

-- Kaç kayıt etkilendi bilgisi:
SELECT COUNT(*) AS etkilenen_kayit
FROM SoruBasvurulari
WHERE IsApproved IS NULL;
