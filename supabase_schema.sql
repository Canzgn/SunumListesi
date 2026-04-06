--
-- PostgreSQL database dump
--

\restrict moN7xgIZVEb3vli4eqUNiCowuiaM0XeH5joGet48cUmMc60jrjAHGaFbDIE8Qv8

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA IF NOT EXISTS public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: adminbolumler; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.adminbolumler (
    adminbolumid integer NOT NULL,
    adminid integer,
    bolumid integer
);


--
-- Name: adminbolumler_adminbolumid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.adminbolumler_adminbolumid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: adminbolumler_adminbolumid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.adminbolumler_adminbolumid_seq OWNED BY public.adminbolumler.adminbolumid;


--
-- Name: admins; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admins (
    adminid integer NOT NULL,
    username character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    isapproved boolean DEFAULT false,
    bolumid integer,
    adsoyad character varying(255)
);


--
-- Name: admins_adminid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.admins_adminid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: admins_adminid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.admins_adminid_seq OWNED BY public.admins.adminid;


--
-- Name: bolumler; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bolumler (
    bolumid integer NOT NULL,
    bolumadi character varying(100) NOT NULL,
    ogretimturu character varying(20) DEFAULT 'Orgün'::character varying NOT NULL,
    donemid integer
);


--
-- Name: bolumler_bolumid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bolumler_bolumid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bolumler_bolumid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bolumler_bolumid_seq OWNED BY public.bolumler.bolumid;


--
-- Name: donemler; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.donemler (
    donemid integer NOT NULL,
    donemadi character varying(20) NOT NULL,
    aktif boolean DEFAULT false,
    basvurubitis timestamp without time zone
);


--
-- Name: donemler_donemid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.donemler_donemid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: donemler_donemid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.donemler_donemid_seq OWNED BY public.donemler.donemid;


--
-- Name: duyurular; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.duyurular (
    duyuruid integer NOT NULL,
    baslik character varying(255) NOT NULL,
    icerik text,
    yayinlayaciadi character varying(100),
    olusturmatarihi timestamp without time zone DEFAULT now(),
    gosterilecekroller character varying(50) DEFAULT 'all'::character varying
);


--
-- Name: duyurular_duyuruid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.duyurular_duyuruid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: duyurular_duyuruid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.duyurular_duyuruid_seq OWNED BY public.duyurular.duyuruid;


--
-- Name: hocabolumler; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hocabolumler (
    hocaid integer NOT NULL,
    bolumid integer NOT NULL
);


--
-- Name: hocalar; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hocalar (
    hocaid integer NOT NULL,
    username character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    adsoyad character varying(255),
    isapproved boolean DEFAULT false
);


--
-- Name: hocalar_hocaid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hocalar_hocaid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hocalar_hocaid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hocalar_hocaid_seq OWNED BY public.hocalar.hocaid;


--
-- Name: islemloglari; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.islemloglari (
    logid integer NOT NULL,
    eylem character varying(100) NOT NULL,
    sunumid integer,
    konuadi character varying(255),
    yapaadi character varying(100),
    detay text,
    zamandamgasi timestamp without time zone DEFAULT now()
);


--
-- Name: islemloglari_logid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.islemloglari_logid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: islemloglari_logid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.islemloglari_logid_seq OWNED BY public.islemloglari.logid;


--
-- Name: konubasvurulari; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.konubasvurulari (
    basvuruid integer NOT NULL,
    sunumid integer,
    ogrenci1no character varying(50),
    ogrenci2no character varying(50) DEFAULT '0'::character varying,
    onceliksirasi integer,
    zamandamgasi timestamp without time zone
);


--
-- Name: konubasvurulari_basvuruid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.konubasvurulari_basvuruid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: konubasvurulari_basvuruid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.konubasvurulari_basvuruid_seq OWNED BY public.konubasvurulari.basvuruid;


--
-- Name: konular; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.konular (
    konuid integer NOT NULL,
    konuadi character varying(255) NOT NULL,
    sirano integer NOT NULL
);


--
-- Name: konular_konuid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.konular_konuid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: konular_konuid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.konular_konuid_seq OWNED BY public.konular.konuid;


--
-- Name: mesajlar; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mesajlar (
    mesajid integer NOT NULL,
    gonderenrol character varying(20) NOT NULL,
    gonderenid integer NOT NULL,
    gonderenadi character varying(255),
    alicirol character varying(20) NOT NULL,
    aliciid integer,
    konu character varying(255) NOT NULL,
    icerik text NOT NULL,
    okundu boolean DEFAULT false,
    gonderimtarihi timestamp without time zone DEFAULT now()
);


--
-- Name: mesajlar_mesajid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mesajlar_mesajid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mesajlar_mesajid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mesajlar_mesajid_seq OWNED BY public.mesajlar.mesajid;


--
-- Name: ogrenciler; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ogrenciler (
    ogrenciid integer NOT NULL,
    ogrencino character varying(50) NOT NULL,
    adsoyad character varying(255),
    ogretimturu character varying(20),
    isapproved boolean DEFAULT false,
    kimlikfoto character varying(255),
    kayittarihi timestamp without time zone,
    password text,
    bolumid integer,
    donemid integer
);


--
-- Name: ogrenciler_ogrenciid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ogrenciler_ogrenciid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ogrenciler_ogrenciid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ogrenciler_ogrenciid_seq OWNED BY public.ogrenciler.ogrenciid;


--
-- Name: sorubasvurulari; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sorubasvurulari (
    sorubasvuruid integer NOT NULL,
    sunumid integer,
    ogrencino character varying(50),
    zamandamgasi timestamp without time zone,
    isapproved boolean DEFAULT true,
    rejectreason character varying(255)
);


--
-- Name: sorubasvurulari_sorubasvuruid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sorubasvurulari_sorubasvuruid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sorubasvurulari_sorubasvuruid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sorubasvurulari_sorubasvuruid_seq OWNED BY public.sorubasvurulari.sorubasvuruid;


--
-- Name: sorukontrolculeri; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sorukontrolculeri (
    kontrolcuid integer NOT NULL,
    username character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    adsoyad character varying(255),
    isapproved boolean DEFAULT true,
    bolumid integer
);


--
-- Name: sorukontrolculeri_kontrolcuid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sorukontrolculeri_kontrolcuid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sorukontrolculeri_kontrolcuid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sorukontrolculeri_kontrolcuid_seq OWNED BY public.sorukontrolculeri.kontrolcuid;


--
-- Name: sunumgorevlileri; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sunumgorevlileri (
    gorevid integer NOT NULL,
    sunumid integer,
    ogrenciid integer
);


--
-- Name: sunumgorevlileri_gorevid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sunumgorevlileri_gorevid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sunumgorevlileri_gorevid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sunumgorevlileri_gorevid_seq OWNED BY public.sunumgorevlileri.gorevid;


--
-- Name: sunumprogrami; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sunumprogrami (
    sunumid integer NOT NULL,
    konuid integer,
    ogretimturu character varying(20) NOT NULL,
    haftano integer NOT NULL,
    bolumid integer,
    sunumtarihi date
);


--
-- Name: sunumprogrami_sunumid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sunumprogrami_sunumid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sunumprogrami_sunumid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sunumprogrami_sunumid_seq OWNED BY public.sunumprogrami.sunumid;


--
-- Name: adminbolumler adminbolumid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.adminbolumler ALTER COLUMN adminbolumid SET DEFAULT nextval('public.adminbolumler_adminbolumid_seq'::regclass);


--
-- Name: admins adminid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admins ALTER COLUMN adminid SET DEFAULT nextval('public.admins_adminid_seq'::regclass);


--
-- Name: bolumler bolumid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bolumler ALTER COLUMN bolumid SET DEFAULT nextval('public.bolumler_bolumid_seq'::regclass);


--
-- Name: donemler donemid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.donemler ALTER COLUMN donemid SET DEFAULT nextval('public.donemler_donemid_seq'::regclass);


--
-- Name: duyurular duyuruid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duyurular ALTER COLUMN duyuruid SET DEFAULT nextval('public.duyurular_duyuruid_seq'::regclass);


--
-- Name: hocalar hocaid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hocalar ALTER COLUMN hocaid SET DEFAULT nextval('public.hocalar_hocaid_seq'::regclass);


--
-- Name: islemloglari logid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.islemloglari ALTER COLUMN logid SET DEFAULT nextval('public.islemloglari_logid_seq'::regclass);


--
-- Name: konubasvurulari basvuruid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konubasvurulari ALTER COLUMN basvuruid SET DEFAULT nextval('public.konubasvurulari_basvuruid_seq'::regclass);


--
-- Name: konular konuid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konular ALTER COLUMN konuid SET DEFAULT nextval('public.konular_konuid_seq'::regclass);


--
-- Name: mesajlar mesajid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mesajlar ALTER COLUMN mesajid SET DEFAULT nextval('public.mesajlar_mesajid_seq'::regclass);


--
-- Name: ogrenciler ogrenciid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ogrenciler ALTER COLUMN ogrenciid SET DEFAULT nextval('public.ogrenciler_ogrenciid_seq'::regclass);


--
-- Name: sorubasvurulari sorubasvuruid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sorubasvurulari ALTER COLUMN sorubasvuruid SET DEFAULT nextval('public.sorubasvurulari_sorubasvuruid_seq'::regclass);


--
-- Name: sorukontrolculeri kontrolcuid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sorukontrolculeri ALTER COLUMN kontrolcuid SET DEFAULT nextval('public.sorukontrolculeri_kontrolcuid_seq'::regclass);


--
-- Name: sunumgorevlileri gorevid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sunumgorevlileri ALTER COLUMN gorevid SET DEFAULT nextval('public.sunumgorevlileri_gorevid_seq'::regclass);


--
-- Name: sunumprogrami sunumid; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sunumprogrami ALTER COLUMN sunumid SET DEFAULT nextval('public.sunumprogrami_sunumid_seq'::regclass);


--
-- Name: adminbolumler adminbolumler_adminid_bolumid_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.adminbolumler
    ADD CONSTRAINT adminbolumler_adminid_bolumid_key UNIQUE (adminid, bolumid);


--
-- Name: adminbolumler adminbolumler_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.adminbolumler
    ADD CONSTRAINT adminbolumler_pkey PRIMARY KEY (adminbolumid);


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (adminid);


--
-- Name: admins admins_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_username_key UNIQUE (username);


--
-- Name: bolumler bolumler_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bolumler
    ADD CONSTRAINT bolumler_pkey PRIMARY KEY (bolumid);


--
-- Name: donemler donemler_donemadi_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.donemler
    ADD CONSTRAINT donemler_donemadi_key UNIQUE (donemadi);


--
-- Name: donemler donemler_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.donemler
    ADD CONSTRAINT donemler_pkey PRIMARY KEY (donemid);


--
-- Name: duyurular duyurular_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duyurular
    ADD CONSTRAINT duyurular_pkey PRIMARY KEY (duyuruid);


--
-- Name: hocabolumler hocabolumler_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hocabolumler
    ADD CONSTRAINT hocabolumler_pkey PRIMARY KEY (hocaid, bolumid);


--
-- Name: hocalar hocalar_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hocalar
    ADD CONSTRAINT hocalar_pkey PRIMARY KEY (hocaid);


--
-- Name: hocalar hocalar_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hocalar
    ADD CONSTRAINT hocalar_username_key UNIQUE (username);


--
-- Name: islemloglari islemloglari_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.islemloglari
    ADD CONSTRAINT islemloglari_pkey PRIMARY KEY (logid);


--
-- Name: konubasvurulari konubasvurulari_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konubasvurulari
    ADD CONSTRAINT konubasvurulari_pkey PRIMARY KEY (basvuruid);


--
-- Name: konular konular_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konular
    ADD CONSTRAINT konular_pkey PRIMARY KEY (konuid);


--
-- Name: mesajlar mesajlar_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mesajlar
    ADD CONSTRAINT mesajlar_pkey PRIMARY KEY (mesajid);


--
-- Name: ogrenciler ogrenciler_ogrencino_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ogrenciler
    ADD CONSTRAINT ogrenciler_ogrencino_key UNIQUE (ogrencino);


--
-- Name: ogrenciler ogrenciler_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ogrenciler
    ADD CONSTRAINT ogrenciler_pkey PRIMARY KEY (ogrenciid);


--
-- Name: sorubasvurulari sorubasvurulari_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sorubasvurulari
    ADD CONSTRAINT sorubasvurulari_pkey PRIMARY KEY (sorubasvuruid);


--
-- Name: sorukontrolculeri sorukontrolculeri_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sorukontrolculeri
    ADD CONSTRAINT sorukontrolculeri_pkey PRIMARY KEY (kontrolcuid);


--
-- Name: sorukontrolculeri sorukontrolculeri_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sorukontrolculeri
    ADD CONSTRAINT sorukontrolculeri_username_key UNIQUE (username);


--
-- Name: sunumgorevlileri sunumgorevlileri_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sunumgorevlileri
    ADD CONSTRAINT sunumgorevlileri_pkey PRIMARY KEY (gorevid);


--
-- Name: sunumprogrami sunumprogrami_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sunumprogrami
    ADD CONSTRAINT sunumprogrami_pkey PRIMARY KEY (sunumid);


--
-- Name: adminbolumler adminbolumler_adminid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.adminbolumler
    ADD CONSTRAINT adminbolumler_adminid_fkey FOREIGN KEY (adminid) REFERENCES public.admins(adminid) ON DELETE CASCADE;


--
-- Name: adminbolumler adminbolumler_bolumid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.adminbolumler
    ADD CONSTRAINT adminbolumler_bolumid_fkey FOREIGN KEY (bolumid) REFERENCES public.bolumler(bolumid) ON DELETE CASCADE;


--
-- Name: admins admins_bolumid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_bolumid_fkey FOREIGN KEY (bolumid) REFERENCES public.bolumler(bolumid) ON DELETE SET NULL;


--
-- Name: bolumler bolumler_donemid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bolumler
    ADD CONSTRAINT bolumler_donemid_fkey FOREIGN KEY (donemid) REFERENCES public.donemler(donemid) ON DELETE SET NULL;


--
-- Name: hocabolumler hocabolumler_bolumid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hocabolumler
    ADD CONSTRAINT hocabolumler_bolumid_fkey FOREIGN KEY (bolumid) REFERENCES public.bolumler(bolumid) ON DELETE CASCADE;


--
-- Name: hocabolumler hocabolumler_hocaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hocabolumler
    ADD CONSTRAINT hocabolumler_hocaid_fkey FOREIGN KEY (hocaid) REFERENCES public.hocalar(hocaid) ON DELETE CASCADE;


--
-- Name: konubasvurulari konubasvurulari_sunumid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konubasvurulari
    ADD CONSTRAINT konubasvurulari_sunumid_fkey FOREIGN KEY (sunumid) REFERENCES public.sunumprogrami(sunumid);


--
-- Name: ogrenciler ogrenciler_bolumid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ogrenciler
    ADD CONSTRAINT ogrenciler_bolumid_fkey FOREIGN KEY (bolumid) REFERENCES public.bolumler(bolumid) ON DELETE SET NULL;


--
-- Name: ogrenciler ogrenciler_donemid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ogrenciler
    ADD CONSTRAINT ogrenciler_donemid_fkey FOREIGN KEY (donemid) REFERENCES public.donemler(donemid) ON DELETE SET NULL;


--
-- Name: sorubasvurulari sorubasvurulari_sunumid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sorubasvurulari
    ADD CONSTRAINT sorubasvurulari_sunumid_fkey FOREIGN KEY (sunumid) REFERENCES public.sunumprogrami(sunumid);


--
-- Name: sorukontrolculeri sorukontrolculeri_bolumid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sorukontrolculeri
    ADD CONSTRAINT sorukontrolculeri_bolumid_fkey FOREIGN KEY (bolumid) REFERENCES public.bolumler(bolumid) ON DELETE SET NULL;


--
-- Name: sunumgorevlileri sunumgorevlileri_ogrenciid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sunumgorevlileri
    ADD CONSTRAINT sunumgorevlileri_ogrenciid_fkey FOREIGN KEY (ogrenciid) REFERENCES public.ogrenciler(ogrenciid);


--
-- Name: sunumgorevlileri sunumgorevlileri_sunumid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sunumgorevlileri
    ADD CONSTRAINT sunumgorevlileri_sunumid_fkey FOREIGN KEY (sunumid) REFERENCES public.sunumprogrami(sunumid);


--
-- Name: sunumprogrami sunumprogrami_bolumid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sunumprogrami
    ADD CONSTRAINT sunumprogrami_bolumid_fkey FOREIGN KEY (bolumid) REFERENCES public.bolumler(bolumid) ON DELETE SET NULL;


--
-- Name: sunumprogrami sunumprogrami_konuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sunumprogrami
    ADD CONSTRAINT sunumprogrami_konuid_fkey FOREIGN KEY (konuid) REFERENCES public.konular(konuid);


--
-- Name: admins; Type: ROW SECURITY; Schema: public; Owner: -
--


--
-- Name: admins backend_full_access; Type: POLICY; Schema: public; Owner: -
--



--
-- Name: konubasvurulari backend_full_access; Type: POLICY; Schema: public; Owner: -
--



--
-- Name: konular backend_full_access; Type: POLICY; Schema: public; Owner: -
--



--
-- Name: ogrenciler backend_full_access; Type: POLICY; Schema: public; Owner: -
--



--
-- Name: sorubasvurulari backend_full_access; Type: POLICY; Schema: public; Owner: -
--



--
-- Name: sunumgorevlileri backend_full_access; Type: POLICY; Schema: public; Owner: -
--



--
-- Name: sunumprogrami backend_full_access; Type: POLICY; Schema: public; Owner: -
--



--
-- Name: konubasvurulari; Type: ROW SECURITY; Schema: public; Owner: -
--


--
-- Name: konular; Type: ROW SECURITY; Schema: public; Owner: -
--


--
-- Name: ogrenciler; Type: ROW SECURITY; Schema: public; Owner: -
--


--
-- Name: sorubasvurulari; Type: ROW SECURITY; Schema: public; Owner: -
--


--
-- Name: sunumgorevlileri; Type: ROW SECURITY; Schema: public; Owner: -
--


--
-- Name: sunumprogrami; Type: ROW SECURITY; Schema: public; Owner: -
--


--
-- PostgreSQL database dump complete
--

\unrestrict moN7xgIZVEb3vli4eqUNiCowuiaM0XeH5joGet48cUmMc60jrjAHGaFbDIE8Qv8

