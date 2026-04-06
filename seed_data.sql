--
-- PostgreSQL database dump
--

\restrict dWITauVBgTGRPH6AhRpw97kHs3DJPhCmm11DgUFFL9Tx6a8k5Kl1E35OXFL23sZ

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
-- Data for Name: donemler; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.donemler VALUES (1, '2025/26', true, NULL);


--
-- Data for Name: bolumler; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.bolumler VALUES (1, 'Bilgisayar Mühendisliği', 'Örgün', 1);
INSERT INTO public.bolumler VALUES (2, 'Bilgisayar Müh. İÖ', 'Gece', 1);
INSERT INTO public.bolumler VALUES (3, 'Yapay Zeka ve Makine Öğrenmesi', 'Örgün', 1);


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.admins VALUES (1, 'admin', 'scrypt:32768:8:1$sTyco9OVndCELQsD$9c395f6036e523ece6dbe06af113c35abee7690938f1e146b61e1c10ce1b1b453527d0e225daae723ae3e56ee7c8b54397880d09fddf19089cbef2dbc3f890b2', true, NULL, NULL);
INSERT INTO public.admins VALUES (2, 'ahmet', 'scrypt:32768:8:1$bmkAuQJ9knwelk3m$5463ec3d68ab97da795f34bcf1f1fefdd03f587c4055adede319d051328b95c6112fb0172e71aeb95080d46d946cfab1b0f426fc9072e066dcd66418fa2174b7', true, 2, NULL);


--
-- Data for Name: adminbolumler; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.adminbolumler VALUES (1, 1, 2);
INSERT INTO public.adminbolumler VALUES (2, 1, 1);
INSERT INTO public.adminbolumler VALUES (3, 2, 3);


--
-- Data for Name: duyurular; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: hocalar; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.hocalar VALUES (1, 'hoca1', 'scrypt:32768:8:1$rbFcB6vRFpYofH16$591f4ecbf20bb15064a9a03594711efbf6665fc194bf2d6c9191b227d533d709e2da154a7b577b4541d6f0d36b6548f1735aa2c5047e6acdb48a7fd74783cef1', 'Öğretmen Hesabı', true);
INSERT INTO public.hocalar VALUES (3, 'uguryildiz', 'scrypt:32768:8:1$BndsZ39Tl9SMejXI$5761ed3749073adb99ff9ebf7bb3a9f95601fcb3c810d70b416b9226a43e30a299d32bd95a04f7c45fb52bbb1e21819aaf15998c39c68d0232b1bb0b10bec17b', 'Öğr. Gör. Uğur Yıldız', true);


--
-- Data for Name: hocabolumler; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.hocabolumler VALUES (1, 1);
INSERT INTO public.hocabolumler VALUES (1, 2);
INSERT INTO public.hocabolumler VALUES (3, 2);
INSERT INTO public.hocabolumler VALUES (3, 1);
INSERT INTO public.hocabolumler VALUES (1, 3);


--
-- Data for Name: islemloglari; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: konular; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.konular VALUES (1, 'Docker Using for Web Development', 1);
INSERT INTO public.konular VALUES (2, 'Git: Github / Gitlab', 2);
INSERT INTO public.konular VALUES (3, 'Bootstrap', 3);
INSERT INTO public.konular VALUES (4, 'Tailwind', 4);
INSERT INTO public.konular VALUES (5, 'JQuery / JQuery UI', 5);
INSERT INTO public.konular VALUES (6, 'TypeScript', 6);
INSERT INTO public.konular VALUES (7, 'Angular', 7);
INSERT INTO public.konular VALUES (8, 'React', 8);
INSERT INTO public.konular VALUES (9, 'Vue', 9);
INSERT INTO public.konular VALUES (10, 'API: JSON APIs', 10);
INSERT INTO public.konular VALUES (11, 'API: REST', 11);
INSERT INTO public.konular VALUES (12, 'API: SOAP', 12);
INSERT INTO public.konular VALUES (13, 'API: gRPC', 13);
INSERT INTO public.konular VALUES (14, 'API: GraphQL', 14);
INSERT INTO public.konular VALUES (15, 'Authentication: HTTP Basic Auth', 15);
INSERT INTO public.konular VALUES (16, 'Authentication: Token Auth', 16);
INSERT INTO public.konular VALUES (17, 'Authentication: JWT', 17);
INSERT INTO public.konular VALUES (18, 'Authentication: OAuth', 18);
INSERT INTO public.konular VALUES (19, 'Authentication: OpenID', 19);
INSERT INTO public.konular VALUES (20, 'Authentication: SAML', 20);
INSERT INTO public.konular VALUES (21, 'Authentication: MFA', 21);
INSERT INTO public.konular VALUES (22, 'Authorization: Role-Based Access Control (RBAC)', 22);
INSERT INTO public.konular VALUES (23, 'Relational Database', 23);
INSERT INTO public.konular VALUES (24, 'ORM: Data Mapper', 24);
INSERT INTO public.konular VALUES (25, 'ORM: Active Record', 25);
INSERT INTO public.konular VALUES (26, 'NoSQL Databases: Document DBs (MongoDB, CouchDB)', 26);
INSERT INTO public.konular VALUES (27, 'NoSQL Databases: Time Series (InfluxDB, TimeScale)', 27);
INSERT INTO public.konular VALUES (28, 'NoSQL Databases: Key-Value (Redis, DynamoDB)', 28);
INSERT INTO public.konular VALUES (29, 'NoSQL Databases: Realtime (Firebase, RethinkDB)', 29);
INSERT INTO public.konular VALUES (30, 'NoSQL Databases: Column DB (Cassandra, HBase)', 30);
INSERT INTO public.konular VALUES (31, 'NoSQL Databases: Graph DB (Neo4j)', 31);
INSERT INTO public.konular VALUES (32, 'Real-Time Data: Long / Short Pooling', 32);
INSERT INTO public.konular VALUES (33, 'Real-Time Data: Server Sent Events', 33);
INSERT INTO public.konular VALUES (34, 'Real-Time Data: Web Sockets', 34);
INSERT INTO public.konular VALUES (35, 'Search Engines: Elasticsearch', 35);
INSERT INTO public.konular VALUES (36, 'Search Engine: Solr', 36);
INSERT INTO public.konular VALUES (37, 'Frameworks: PHP (Laravel / Yii)', 37);
INSERT INTO public.konular VALUES (38, 'Frameworks: Java (Spring Boots)', 38);
INSERT INTO public.konular VALUES (39, 'Frameworks: C# (DotNet Core)', 39);
INSERT INTO public.konular VALUES (40, 'Framework: Python (Django)', 40);
INSERT INTO public.konular VALUES (41, 'Framework: JS (NodeJS)', 41);
INSERT INTO public.konular VALUES (42, 'Package / Dependency Management (NPM / PNPM / Yarn / NuGet / Composer)', 42);
INSERT INTO public.konular VALUES (43, 'Web Servers: Apache / Nginx / MS ISS', 43);
INSERT INTO public.konular VALUES (44, 'Security: Enjeksiyon Saldırıları (SQL Injection (SQLi) / Command Injection)', 44);
INSERT INTO public.konular VALUES (45, 'Security: Cross-Site Scripting (Stored XSS / Reflected XSS)', 45);
INSERT INTO public.konular VALUES (46, 'Security: Cross-Site Request Forgery (CSRF)', 46);
INSERT INTO public.konular VALUES (47, 'Security: Kimlik Doğrulama ve Oturum Yönetimi Hataları (Broken Authentication / JWT (JSON Web Token) Güvenliği)', 47);
INSERT INTO public.konular VALUES (48, 'Security: Sensitive Data Exposure (HTTPS/TLS / Hashing vs Encryption)', 48);
INSERT INTO public.konular VALUES (49, 'Security: Insecure Deserialization', 49);
INSERT INTO public.konular VALUES (50, 'Security: Security Misconfiguration', 50);
INSERT INTO public.konular VALUES (51, 'Security: API Güvenliği (Rate Limiting / CORS (Cross-Origin Resource Sharing))', 51);
INSERT INTO public.konular VALUES (52, 'UI / UX Tasarımı', 52);
INSERT INTO public.konular VALUES (53, 'Digital Wireframing: Figma', 53);
INSERT INTO public.konular VALUES (54, 'Digital Wireframing: Balsamiq', 54);
INSERT INTO public.konular VALUES (55, 'Privacy Policies', 55);
INSERT INTO public.konular VALUES (56, 'Testing: Unit / Integration / End-to-End', 56);
INSERT INTO public.konular VALUES (57, 'Test Metodolojileri: Test Driven Development / Behavior Driven Development', 57);
INSERT INTO public.konular VALUES (58, 'API ve Backend Testing: Contract / Mocking / Load & Performance', 58);
INSERT INTO public.konular VALUES (59, 'QA & Automation: Code Review / Static Code Analysis / CI/CD', 59);
INSERT INTO public.konular VALUES (60, 'Manuel QA ve Usability Testing: Exploratory / UI/UX / Accessibility (A11y)', 60);


--
-- Data for Name: sunumprogrami; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.sunumprogrami VALUES (361, 1, 'Örgün', 1, 1, '2026-03-06');
INSERT INTO public.sunumprogrami VALUES (363, 2, 'Örgün', 1, 1, '2026-03-06');
INSERT INTO public.sunumprogrami VALUES (365, 3, 'Örgün', 1, 1, '2026-03-06');
INSERT INTO public.sunumprogrami VALUES (367, 4, 'Örgün', 1, 1, '2026-03-06');
INSERT INTO public.sunumprogrami VALUES (369, 5, 'Örgün', 2, 1, '2026-03-13');
INSERT INTO public.sunumprogrami VALUES (371, 6, 'Örgün', 2, 1, '2026-03-13');
INSERT INTO public.sunumprogrami VALUES (373, 7, 'Örgün', 2, 1, '2026-03-13');
INSERT INTO public.sunumprogrami VALUES (375, 8, 'Örgün', 2, 1, '2026-03-13');
INSERT INTO public.sunumprogrami VALUES (377, 9, 'Örgün', 3, 1, '2026-03-27');
INSERT INTO public.sunumprogrami VALUES (379, 10, 'Örgün', 3, 1, '2026-03-27');
INSERT INTO public.sunumprogrami VALUES (381, 11, 'Örgün', 3, 1, '2026-03-27');
INSERT INTO public.sunumprogrami VALUES (383, 12, 'Örgün', 3, 1, '2026-03-27');
INSERT INTO public.sunumprogrami VALUES (385, 13, 'Örgün', 4, 1, '2026-04-03');
INSERT INTO public.sunumprogrami VALUES (387, 14, 'Örgün', 4, 1, '2026-04-03');
INSERT INTO public.sunumprogrami VALUES (389, 15, 'Örgün', 4, 1, '2026-04-03');
INSERT INTO public.sunumprogrami VALUES (391, 16, 'Örgün', 4, 1, '2026-04-03');
INSERT INTO public.sunumprogrami VALUES (393, 17, 'Örgün', 5, 1, '2026-04-10');
INSERT INTO public.sunumprogrami VALUES (395, 18, 'Örgün', 5, 1, '2026-04-10');
INSERT INTO public.sunumprogrami VALUES (397, 19, 'Örgün', 5, 1, '2026-04-10');
INSERT INTO public.sunumprogrami VALUES (399, 20, 'Örgün', 5, 1, '2026-04-10');
INSERT INTO public.sunumprogrami VALUES (401, 21, 'Örgün', 6, 1, '2026-04-17');
INSERT INTO public.sunumprogrami VALUES (403, 22, 'Örgün', 6, 1, '2026-04-17');
INSERT INTO public.sunumprogrami VALUES (405, 23, 'Örgün', 6, 1, '2026-04-17');
INSERT INTO public.sunumprogrami VALUES (407, 24, 'Örgün', 6, 1, '2026-04-17');
INSERT INTO public.sunumprogrami VALUES (409, 25, 'Örgün', 7, 1, '2026-04-24');
INSERT INTO public.sunumprogrami VALUES (411, 26, 'Örgün', 7, 1, '2026-04-24');
INSERT INTO public.sunumprogrami VALUES (413, 27, 'Örgün', 7, 1, '2026-04-24');
INSERT INTO public.sunumprogrami VALUES (415, 28, 'Örgün', 7, 1, '2026-04-24');
INSERT INTO public.sunumprogrami VALUES (417, 29, 'Örgün', 8, 1, '2026-05-01');
INSERT INTO public.sunumprogrami VALUES (419, 30, 'Örgün', 8, 1, '2026-05-01');
INSERT INTO public.sunumprogrami VALUES (421, 31, 'Örgün', 8, 1, '2026-05-01');
INSERT INTO public.sunumprogrami VALUES (423, 32, 'Örgün', 8, 1, '2026-05-01');
INSERT INTO public.sunumprogrami VALUES (425, 33, 'Örgün', 9, 1, '2026-05-08');
INSERT INTO public.sunumprogrami VALUES (427, 34, 'Örgün', 9, 1, '2026-05-08');
INSERT INTO public.sunumprogrami VALUES (429, 35, 'Örgün', 9, 1, '2026-05-08');
INSERT INTO public.sunumprogrami VALUES (431, 36, 'Örgün', 9, 1, '2026-05-08');
INSERT INTO public.sunumprogrami VALUES (433, 37, 'Örgün', 10, 1, '2026-05-15');
INSERT INTO public.sunumprogrami VALUES (460, 50, 'Gece', 13, 2, '2026-06-05');
INSERT INTO public.sunumprogrami VALUES (462, 51, 'Gece', 13, 2, '2026-06-05');
INSERT INTO public.sunumprogrami VALUES (464, 52, 'Gece', 13, 2, '2026-06-05');
INSERT INTO public.sunumprogrami VALUES (465, 53, 'Örgün', 14, 1, '2026-06-12');
INSERT INTO public.sunumprogrami VALUES (467, 54, 'Örgün', 14, 1, '2026-06-12');
INSERT INTO public.sunumprogrami VALUES (469, 55, 'Örgün', 14, 1, '2026-06-12');
INSERT INTO public.sunumprogrami VALUES (471, 56, 'Örgün', 14, 1, '2026-06-12');
INSERT INTO public.sunumprogrami VALUES (466, 53, 'Gece', 14, 2, '2026-06-12');
INSERT INTO public.sunumprogrami VALUES (468, 54, 'Gece', 14, 2, '2026-06-12');
INSERT INTO public.sunumprogrami VALUES (470, 55, 'Gece', 14, 2, '2026-06-12');
INSERT INTO public.sunumprogrami VALUES (472, 56, 'Gece', 14, 2, '2026-06-12');
INSERT INTO public.sunumprogrami VALUES (473, 57, 'Örgün', 15, 1, '2026-06-19');
INSERT INTO public.sunumprogrami VALUES (475, 58, 'Örgün', 15, 1, '2026-06-19');
INSERT INTO public.sunumprogrami VALUES (477, 59, 'Örgün', 15, 1, '2026-06-19');
INSERT INTO public.sunumprogrami VALUES (479, 60, 'Örgün', 15, 1, '2026-06-19');
INSERT INTO public.sunumprogrami VALUES (474, 57, 'Gece', 15, 2, '2026-06-19');
INSERT INTO public.sunumprogrami VALUES (476, 58, 'Gece', 15, 2, '2026-06-19');
INSERT INTO public.sunumprogrami VALUES (478, 59, 'Gece', 15, 2, '2026-06-19');
INSERT INTO public.sunumprogrami VALUES (480, 60, 'Gece', 15, 2, '2026-06-19');
INSERT INTO public.sunumprogrami VALUES (364, 2, 'Gece', 1, 2, '2026-03-06');
INSERT INTO public.sunumprogrami VALUES (366, 3, 'Gece', 1, 2, '2026-03-06');
INSERT INTO public.sunumprogrami VALUES (368, 4, 'Gece', 1, 2, '2026-03-06');
INSERT INTO public.sunumprogrami VALUES (362, 1, 'Gece', 1, 2, '2026-03-06');
INSERT INTO public.sunumprogrami VALUES (370, 5, 'Gece', 2, 2, '2026-03-13');
INSERT INTO public.sunumprogrami VALUES (372, 6, 'Gece', 2, 2, '2026-03-13');
INSERT INTO public.sunumprogrami VALUES (374, 7, 'Gece', 2, 2, '2026-03-13');
INSERT INTO public.sunumprogrami VALUES (376, 8, 'Gece', 2, 2, '2026-03-13');
INSERT INTO public.sunumprogrami VALUES (378, 9, 'Gece', 3, 2, '2026-03-27');
INSERT INTO public.sunumprogrami VALUES (380, 10, 'Gece', 3, 2, '2026-03-27');
INSERT INTO public.sunumprogrami VALUES (382, 11, 'Gece', 3, 2, '2026-03-27');
INSERT INTO public.sunumprogrami VALUES (384, 12, 'Gece', 3, 2, '2026-03-27');
INSERT INTO public.sunumprogrami VALUES (386, 13, 'Gece', 4, 2, '2026-04-03');
INSERT INTO public.sunumprogrami VALUES (388, 14, 'Gece', 4, 2, '2026-04-03');
INSERT INTO public.sunumprogrami VALUES (390, 15, 'Gece', 4, 2, '2026-04-03');
INSERT INTO public.sunumprogrami VALUES (392, 16, 'Gece', 4, 2, '2026-04-03');
INSERT INTO public.sunumprogrami VALUES (394, 17, 'Gece', 5, 2, '2026-04-10');
INSERT INTO public.sunumprogrami VALUES (396, 18, 'Gece', 5, 2, '2026-04-10');
INSERT INTO public.sunumprogrami VALUES (398, 19, 'Gece', 5, 2, '2026-04-10');
INSERT INTO public.sunumprogrami VALUES (400, 20, 'Gece', 5, 2, '2026-04-10');
INSERT INTO public.sunumprogrami VALUES (402, 21, 'Gece', 6, 2, '2026-04-17');
INSERT INTO public.sunumprogrami VALUES (404, 22, 'Gece', 6, 2, '2026-04-17');
INSERT INTO public.sunumprogrami VALUES (406, 23, 'Gece', 6, 2, '2026-04-17');
INSERT INTO public.sunumprogrami VALUES (408, 24, 'Gece', 6, 2, '2026-04-17');
INSERT INTO public.sunumprogrami VALUES (410, 25, 'Gece', 7, 2, '2026-04-24');
INSERT INTO public.sunumprogrami VALUES (412, 26, 'Gece', 7, 2, '2026-04-24');
INSERT INTO public.sunumprogrami VALUES (414, 27, 'Gece', 7, 2, '2026-04-24');
INSERT INTO public.sunumprogrami VALUES (416, 28, 'Gece', 7, 2, '2026-04-24');
INSERT INTO public.sunumprogrami VALUES (418, 29, 'Gece', 8, 2, '2026-05-01');
INSERT INTO public.sunumprogrami VALUES (420, 30, 'Gece', 8, 2, '2026-05-01');
INSERT INTO public.sunumprogrami VALUES (422, 31, 'Gece', 8, 2, '2026-05-01');
INSERT INTO public.sunumprogrami VALUES (424, 32, 'Gece', 8, 2, '2026-05-01');
INSERT INTO public.sunumprogrami VALUES (426, 33, 'Gece', 9, 2, '2026-05-08');
INSERT INTO public.sunumprogrami VALUES (428, 34, 'Gece', 9, 2, '2026-05-08');
INSERT INTO public.sunumprogrami VALUES (430, 35, 'Gece', 9, 2, '2026-05-08');
INSERT INTO public.sunumprogrami VALUES (432, 36, 'Gece', 9, 2, '2026-05-08');
INSERT INTO public.sunumprogrami VALUES (435, 38, 'Örgün', 10, 1, '2026-05-15');
INSERT INTO public.sunumprogrami VALUES (437, 39, 'Örgün', 10, 1, '2026-05-15');
INSERT INTO public.sunumprogrami VALUES (439, 40, 'Örgün', 10, 1, '2026-05-15');
INSERT INTO public.sunumprogrami VALUES (434, 37, 'Gece', 10, 2, '2026-05-15');
INSERT INTO public.sunumprogrami VALUES (436, 38, 'Gece', 10, 2, '2026-05-15');
INSERT INTO public.sunumprogrami VALUES (438, 39, 'Gece', 10, 2, '2026-05-15');
INSERT INTO public.sunumprogrami VALUES (440, 40, 'Gece', 10, 2, '2026-05-15');
INSERT INTO public.sunumprogrami VALUES (441, 41, 'Örgün', 11, 1, '2026-05-22');
INSERT INTO public.sunumprogrami VALUES (443, 42, 'Örgün', 11, 1, '2026-05-22');
INSERT INTO public.sunumprogrami VALUES (445, 43, 'Örgün', 11, 1, '2026-05-22');
INSERT INTO public.sunumprogrami VALUES (447, 44, 'Örgün', 11, 1, '2026-05-22');
INSERT INTO public.sunumprogrami VALUES (442, 41, 'Gece', 11, 2, '2026-05-22');
INSERT INTO public.sunumprogrami VALUES (444, 42, 'Gece', 11, 2, '2026-05-22');
INSERT INTO public.sunumprogrami VALUES (446, 43, 'Gece', 11, 2, '2026-05-22');
INSERT INTO public.sunumprogrami VALUES (448, 44, 'Gece', 11, 2, '2026-05-22');
INSERT INTO public.sunumprogrami VALUES (449, 45, 'Örgün', 12, 1, '2026-05-29');
INSERT INTO public.sunumprogrami VALUES (451, 46, 'Örgün', 12, 1, '2026-05-29');
INSERT INTO public.sunumprogrami VALUES (453, 47, 'Örgün', 12, 1, '2026-05-29');
INSERT INTO public.sunumprogrami VALUES (455, 48, 'Örgün', 12, 1, '2026-05-29');
INSERT INTO public.sunumprogrami VALUES (450, 45, 'Gece', 12, 2, '2026-05-29');
INSERT INTO public.sunumprogrami VALUES (452, 46, 'Gece', 12, 2, '2026-05-29');
INSERT INTO public.sunumprogrami VALUES (454, 47, 'Gece', 12, 2, '2026-05-29');
INSERT INTO public.sunumprogrami VALUES (456, 48, 'Gece', 12, 2, '2026-05-29');
INSERT INTO public.sunumprogrami VALUES (457, 49, 'Örgün', 13, 1, '2026-06-05');
INSERT INTO public.sunumprogrami VALUES (459, 50, 'Örgün', 13, 1, '2026-06-05');
INSERT INTO public.sunumprogrami VALUES (461, 51, 'Örgün', 13, 1, '2026-06-05');
INSERT INTO public.sunumprogrami VALUES (463, 52, 'Örgün', 13, 1, '2026-06-05');
INSERT INTO public.sunumprogrami VALUES (458, 49, 'Gece', 13, 2, '2026-06-05');


--
-- Data for Name: konubasvurulari; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.konubasvurulari VALUES (877, 429, '230201035', '220201094', 1, '2026-03-11 02:06:50');
INSERT INTO public.konubasvurulari VALUES (878, 433, '230201064', '230201049', 1, '2026-03-12 04:38:46');
INSERT INTO public.konubasvurulari VALUES (879, 362, '210202064', '0', 2, '2026-03-13 14:12:57');
INSERT INTO public.konubasvurulari VALUES (880, 384, '230202098', '230202042', 2, '2026-03-15 15:32:20');
INSERT INTO public.konubasvurulari VALUES (881, 406, '230202020', '230202051', 2, '2026-03-18 05:52:33');
INSERT INTO public.konubasvurulari VALUES (882, 409, '230201087', '230201089', 1, '2026-03-24 22:10:37');
INSERT INTO public.konubasvurulari VALUES (731, 374, '230202017', '230202026', 1, '2026-03-03 16:35:00');
INSERT INTO public.konubasvurulari VALUES (732, 386, '230202093', '230202050', 1, '2026-03-03 22:33:31');
INSERT INTO public.konubasvurulari VALUES (733, 381, '240201132', '230201095', 1, '2026-03-03 17:08:24');
INSERT INTO public.konubasvurulari VALUES (734, 381, '230201034', '230201098', 2, '2026-03-04 00:20:05');
INSERT INTO public.konubasvurulari VALUES (735, 381, '220201007', '220201050', 3, '2026-03-04 00:43:53');
INSERT INTO public.konubasvurulari VALUES (736, 381, '210201083', '210201083', 4, '2026-03-05 22:31:44');
INSERT INTO public.konubasvurulari VALUES (737, 382, '230202107', '230202043', 1, '2026-03-03 21:59:41');
INSERT INTO public.konubasvurulari VALUES (738, 382, '220202040', '220202013', 2, '2026-03-04 17:19:55');
INSERT INTO public.konubasvurulari VALUES (739, 382, '230202104', '0', 3, '2026-03-05 22:33:29');
INSERT INTO public.konubasvurulari VALUES (740, 382, '240202016', '0', 4, '2026-03-09 23:54:42');
INSERT INTO public.konubasvurulari VALUES (741, 394, '240202001', '230202084', 1, '2026-03-03 18:37:03');
INSERT INTO public.konubasvurulari VALUES (742, 362, '230202022', '230202091', 1, '2026-03-03 22:23:26');
INSERT INTO public.konubasvurulari VALUES (743, 442, '220202028', '220202028', 1, '2026-03-03 18:41:08');
INSERT INTO public.konubasvurulari VALUES (744, 440, '230202064', '230202065', 1, '2026-03-03 21:34:47');
INSERT INTO public.konubasvurulari VALUES (745, 438, '230202108', '230202114', 1, '2026-03-03 16:30:19');
INSERT INTO public.konubasvurulari VALUES (746, 436, '230202048', '230202033', 1, '2026-03-03 18:51:18');
INSERT INTO public.konubasvurulari VALUES (747, 418, '230202013', '230202007', 1, '2026-03-03 18:52:36');
INSERT INTO public.konubasvurulari VALUES (748, 418, '230202054', '230202047', 2, '2026-03-04 23:43:13');
INSERT INTO public.konubasvurulari VALUES (749, 470, '230202109', '230202109', 1, '2026-03-03 20:03:26');
INSERT INTO public.konubasvurulari VALUES (750, 470, '220202110', '220202110', 2, '2026-03-06 17:16:38');
INSERT INTO public.konubasvurulari VALUES (751, 376, '230202023', '230202078', 1, '2026-03-03 16:53:04');
INSERT INTO public.konubasvurulari VALUES (752, 406, '220202076', '220202076', 1, '2026-03-03 22:29:35');
INSERT INTO public.konubasvurulari VALUES (753, 462, '230202073', '230202103', 1, '2026-03-03 16:51:26');
INSERT INTO public.konubasvurulari VALUES (754, 452, '230202071', '230202101', 1, '2026-03-03 18:58:21');
INSERT INTO public.konubasvurulari VALUES (755, 450, '230202131', '230202012', 1, '2026-03-03 22:40:44');
INSERT INTO public.konubasvurulari VALUES (756, 448, '230202076', '230202126', 1, '2026-03-03 21:45:41');
INSERT INTO public.konubasvurulari VALUES (757, 454, '230202066', '230202095', 1, '2026-03-03 16:47:34');
INSERT INTO public.konubasvurulari VALUES (758, 368, '230202039', '230202097', 1, '2026-03-03 22:37:51');
INSERT INTO public.konubasvurulari VALUES (759, 464, '230202021', '230202061', 1, '2026-03-03 22:26:18');
INSERT INTO public.konubasvurulari VALUES (760, 370, '230202113', '0', 1, '2026-03-03 23:23:28');
INSERT INTO public.konubasvurulari VALUES (761, 370, '230202113', '210202049', 2, '2026-03-05 13:20:48');
INSERT INTO public.konubasvurulari VALUES (762, 370, '230202030', '230202113', 3, '2026-03-09 14:59:46');
INSERT INTO public.konubasvurulari VALUES (763, 445, '230201061', '230201048', 1, '2026-03-03 23:49:52');
INSERT INTO public.konubasvurulari VALUES (764, 449, '230201075', '230201041', 1, '2026-03-04 00:00:03');
INSERT INTO public.konubasvurulari VALUES (765, 403, '230201009', '230201004', 1, '2026-03-04 00:03:32');
INSERT INTO public.konubasvurulari VALUES (766, 403, '230201087', '230201089', 2, '2026-03-04 13:26:01');
INSERT INTO public.konubasvurulari VALUES (767, 369, '220201028', '220201028', 1, '2026-03-04 00:03:55');
INSERT INTO public.konubasvurulari VALUES (768, 465, '230201020', '230201024', 1, '2026-03-04 00:03:59');
INSERT INTO public.konubasvurulari VALUES (769, 465, '230201022', '230201066', 2, '2026-03-04 00:04:00');
INSERT INTO public.konubasvurulari VALUES (770, 435, '230201093', '230201117', 1, '2026-03-04 00:05:14');
INSERT INTO public.konubasvurulari VALUES (771, 435, '230201102', '230201107', 2, '2026-03-04 00:14:28');
INSERT INTO public.konubasvurulari VALUES (772, 437, '220201068', '230201081', 1, '2026-03-04 00:06:18');
INSERT INTO public.konubasvurulari VALUES (773, 437, '220201007', '220201050', 2, '2026-03-04 00:54:01');
INSERT INTO public.konubasvurulari VALUES (774, 463, '230201022', '230201066', 1, '2026-03-04 00:08:07');
INSERT INTO public.konubasvurulari VALUES (775, 375, '230201037', '230201088', 1, '2026-03-04 00:09:58');
INSERT INTO public.konubasvurulari VALUES (776, 363, '230201112', '0', 1, '2026-03-04 00:12:23');
INSERT INTO public.konubasvurulari VALUES (777, 363, '230201112', '230201097', 2, '2026-03-04 10:51:40');
INSERT INTO public.konubasvurulari VALUES (778, 447, '230201082', '230201031', 1, '2026-03-04 00:14:12');
INSERT INTO public.konubasvurulari VALUES (779, 453, '230201033', '230201058', 1, '2026-03-04 00:15:53');
INSERT INTO public.konubasvurulari VALUES (780, 377, '230201027', '230201023', 1, '2026-03-04 00:21:15');
INSERT INTO public.konubasvurulari VALUES (781, 439, '230201102', '230201107', 1, '2026-03-04 00:21:35');
INSERT INTO public.konubasvurulari VALUES (782, 439, '220201142', '230201074', 2, '2026-03-04 08:04:51');
INSERT INTO public.konubasvurulari VALUES (783, 389, '230201057', '220201087', 1, '2026-03-04 00:23:16');
INSERT INTO public.konubasvurulari VALUES (784, 461, '240201124', '230201054', 1, '2026-03-04 00:25:11');
INSERT INTO public.konubasvurulari VALUES (785, 461, '230201046', '230201123', 2, '2026-03-04 00:51:02');
INSERT INTO public.konubasvurulari VALUES (786, 371, '220201144', '220201146', 1, '2026-03-04 00:29:02');
INSERT INTO public.konubasvurulari VALUES (787, 365, '220201075', '210201049', 1, '2026-03-04 00:30:00');
INSERT INTO public.konubasvurulari VALUES (788, 473, '230201154', '220201046', 1, '2026-03-04 00:34:08');
INSERT INTO public.konubasvurulari VALUES (789, 372, '240202004', '230202112', 1, '2026-03-04 00:38:35');
INSERT INTO public.konubasvurulari VALUES (790, 396, '230202010', '240202012', 1, '2026-03-04 00:41:08');
INSERT INTO public.konubasvurulari VALUES (791, 415, '220201042', '220201054', 1, '2026-03-04 00:41:31');
INSERT INTO public.konubasvurulari VALUES (792, 443, '230201092', '230201090', 1, '2026-03-04 00:49:20');
INSERT INTO public.konubasvurulari VALUES (793, 367, '230201111', '230201062', 1, '2026-03-04 00:50:37');
INSERT INTO public.konubasvurulari VALUES (794, 427, '230201046', '230201123', 1, '2026-03-04 00:55:09');
INSERT INTO public.konubasvurulari VALUES (795, 395, '220201007', '220201050', 1, '2026-03-04 01:01:52');
INSERT INTO public.konubasvurulari VALUES (796, 387, '230201078', '240201119', 1, '2026-03-04 01:07:59');
INSERT INTO public.konubasvurulari VALUES (797, 431, '230201101', '230201051', 1, '2026-03-04 01:09:25');
INSERT INTO public.konubasvurulari VALUES (798, 391, '230201076', '240201120', 1, '2026-03-04 01:13:26');
INSERT INTO public.konubasvurulari VALUES (799, 469, '230201085', '230201080', 1, '2026-03-04 01:41:50');
INSERT INTO public.konubasvurulari VALUES (800, 361, '210201142', '230201070', 1, '2026-03-04 01:52:41');
INSERT INTO public.konubasvurulari VALUES (801, 467, '250201110', '240201122', 1, '2026-03-04 02:07:00');
INSERT INTO public.konubasvurulari VALUES (802, 379, '230201103', '230201105', 1, '2026-03-04 03:07:58');
INSERT INTO public.konubasvurulari VALUES (803, 477, '220201142', '230201074', 1, '2026-03-04 08:28:50');
INSERT INTO public.konubasvurulari VALUES (804, 428, '230202046', '230202062', 1, '2026-03-04 10:12:09');
INSERT INTO public.konubasvurulari VALUES (805, 402, '230202045', '230202088', 1, '2026-03-04 11:13:32');
INSERT INTO public.konubasvurulari VALUES (806, 411, '230201040', '230201072', 1, '2026-03-04 11:35:04');
INSERT INTO public.konubasvurulari VALUES (807, 364, '230202037', '230202105', 1, '2026-03-04 12:07:10');
INSERT INTO public.konubasvurulari VALUES (808, 364, '230202038', '230202080', 2, '2026-03-05 11:34:13');
INSERT INTO public.konubasvurulari VALUES (809, 364, '240202013', '230202079', 3, '2026-03-05 15:21:57');
INSERT INTO public.konubasvurulari VALUES (810, 459, '230201097', '201230114', 1, '2026-03-04 12:07:25');
INSERT INTO public.konubasvurulari VALUES (811, 393, '230201065', '230201099', 1, '2026-03-04 12:09:51');
INSERT INTO public.konubasvurulari VALUES (812, 410, '230202068', '230202068', 1, '2026-03-04 12:33:32');
INSERT INTO public.konubasvurulari VALUES (813, 410, '230202068', '220202076', 2, '2026-03-06 20:31:47');
INSERT INTO public.konubasvurulari VALUES (814, 401, '230201139', '230201139', 1, '2026-03-04 12:59:43');
INSERT INTO public.konubasvurulari VALUES (815, 401, '230201139', '230201029', 2, '2026-03-04 13:23:42');
INSERT INTO public.konubasvurulari VALUES (816, 407, '230201030', '230201032', 1, '2026-03-04 13:10:31');
INSERT INTO public.konubasvurulari VALUES (817, 366, '220202091', '0', 1, '2026-03-04 13:13:02');
INSERT INTO public.konubasvurulari VALUES (818, 366, '220202091', '210202049', 2, '2026-03-05 13:22:16');
INSERT INTO public.konubasvurulari VALUES (819, 380, '230202001', '230202044', 1, '2026-03-04 13:23:48');
INSERT INTO public.konubasvurulari VALUES (820, 390, '230202058', '230202081', 1, '2026-03-04 13:30:06');
INSERT INTO public.konubasvurulari VALUES (821, 441, '230201053', '230201073', 1, '2026-03-04 13:48:28');
INSERT INTO public.konubasvurulari VALUES (822, 441, '230201049', '230201064', 2, '2026-03-04 22:34:57');
INSERT INTO public.konubasvurulari VALUES (823, 426, '230202083', '230202082', 1, '2026-03-04 13:51:23');
INSERT INTO public.konubasvurulari VALUES (824, 398, '230202070', '230202049', 1, '2026-03-04 13:58:45');
INSERT INTO public.konubasvurulari VALUES (825, 466, '230202057', '230202036', 1, '2026-03-04 13:58:46');
INSERT INTO public.konubasvurulari VALUES (826, 451, '230201069', '230201055', 1, '2026-03-04 14:07:20');
INSERT INTO public.konubasvurulari VALUES (827, 404, '230202016', '230202035', 1, '2026-03-04 14:37:01');
INSERT INTO public.konubasvurulari VALUES (828, 423, '230201109', '0', 1, '2026-03-04 15:31:59');
INSERT INTO public.konubasvurulari VALUES (829, 455, '240201123', '230201104', 1, '2026-03-04 15:51:43');
INSERT INTO public.konubasvurulari VALUES (830, 412, '220202103', '0', 1, '2026-03-04 16:28:18');
INSERT INTO public.konubasvurulari VALUES (831, 412, '220202103', '210202049', 2, '2026-03-05 13:23:18');
INSERT INTO public.konubasvurulari VALUES (832, 444, '240202005', '240202003', 1, '2026-03-04 17:03:13');
INSERT INTO public.konubasvurulari VALUES (833, 416, '220202040', '220202013', 1, '2026-03-04 17:23:51');
INSERT INTO public.konubasvurulari VALUES (834, 416, '230202077', '230202075', 2, '2026-03-08 17:38:03');
INSERT INTO public.konubasvurulari VALUES (835, 388, '230202129', '230202047', 1, '2026-03-04 18:14:05');
INSERT INTO public.konubasvurulari VALUES (836, 388, '230202056', '0', 2, '2026-03-06 18:56:39');
INSERT INTO public.konubasvurulari VALUES (837, 430, '230202084', '230202091', 1, '2026-03-04 18:16:50');
INSERT INTO public.konubasvurulari VALUES (838, 434, '230202075', '230202020', 1, '2026-03-04 18:17:31');
INSERT INTO public.konubasvurulari VALUES (839, 446, '230202112', '220202053', 1, '2026-03-04 18:17:58');
INSERT INTO public.konubasvurulari VALUES (840, 474, '230202105', '230202053', 1, '2026-03-04 18:18:34');
INSERT INTO public.konubasvurulari VALUES (841, 468, '220202017', '220202040', 1, '2026-03-04 18:19:15');
INSERT INTO public.konubasvurulari VALUES (842, 468, '230202060', '0', 2, '2026-03-05 00:53:59');
INSERT INTO public.konubasvurulari VALUES (843, 373, '240201120', '230201049', 1, '2026-03-04 18:19:49');
INSERT INTO public.konubasvurulari VALUES (844, 385, '230201035', '230201023', 1, '2026-03-04 18:20:17');
INSERT INTO public.konubasvurulari VALUES (845, 417, '220201082', '230201049', 1, '2026-03-04 18:21:06');
INSERT INTO public.konubasvurulari VALUES (846, 378, '220202083', '230201130', 1, '2026-03-04 18:22:48');
INSERT INTO public.konubasvurulari VALUES (847, 421, '230201131', '240201120', 1, '2026-03-04 18:45:14');
INSERT INTO public.konubasvurulari VALUES (848, 421, '230201071', '230201131', 2, '2026-03-08 17:03:42');
INSERT INTO public.konubasvurulari VALUES (849, 397, '230201054', '220201080', 1, '2026-03-04 19:47:44');
INSERT INTO public.konubasvurulari VALUES (850, 392, '220202027', '210202051', 1, '2026-03-04 20:23:32');
INSERT INTO public.konubasvurulari VALUES (851, 425, '220201006', '220201074', 1, '2026-03-04 21:08:01');
INSERT INTO public.konubasvurulari VALUES (852, 408, '230202019', '230202031', 1, '2026-03-04 21:27:31');
INSERT INTO public.konubasvurulari VALUES (853, 478, '230202027', '230202053', 1, '2026-03-04 23:22:04');
INSERT INTO public.konubasvurulari VALUES (854, 456, '230202111', '210202045', 1, '2026-03-04 23:36:42');
INSERT INTO public.konubasvurulari VALUES (855, 476, '230202067', '230202052', 1, '2026-03-05 01:00:12');
INSERT INTO public.konubasvurulari VALUES (856, 460, '230202063', '230202129', 1, '2026-03-05 13:08:53');
INSERT INTO public.konubasvurulari VALUES (857, 472, '230202018', '230202100', 1, '2026-03-05 13:40:01');
INSERT INTO public.konubasvurulari VALUES (858, 480, '230202029', '0', 1, '2026-03-05 13:44:12');
INSERT INTO public.konubasvurulari VALUES (859, 480, '230202029', '220202085', 2, '2026-03-06 17:29:59');
INSERT INTO public.konubasvurulari VALUES (860, 414, '220202031', '220202017', 1, '2026-03-05 14:51:22');
INSERT INTO public.konubasvurulari VALUES (861, 424, '230202040', '230202069', 1, '2026-03-05 15:40:51');
INSERT INTO public.konubasvurulari VALUES (862, 458, '230202074', '230202086', 1, '2026-03-05 22:42:17');
INSERT INTO public.konubasvurulari VALUES (863, 420, '230202080', '230202038', 1, '2026-03-05 22:44:44');
INSERT INTO public.konubasvurulari VALUES (864, 479, '230201089', '230201087', 1, '2026-03-05 22:49:27');
INSERT INTO public.konubasvurulari VALUES (865, 475, '230201067', '0', 1, '2026-03-05 23:47:52');
INSERT INTO public.konubasvurulari VALUES (866, 471, '210201010', '210201037', 1, '2026-03-06 00:32:08');
INSERT INTO public.konubasvurulari VALUES (867, 383, '210201049', '220201075', 1, '2026-03-06 00:58:50');
INSERT INTO public.konubasvurulari VALUES (868, 405, '220201043', '220201082', 1, '2026-03-06 13:02:36');
INSERT INTO public.konubasvurulari VALUES (869, 399, '210201083', '210201064', 1, '2026-03-06 15:03:08');
INSERT INTO public.konubasvurulari VALUES (870, 432, '230202087', '230202104', 1, '2026-03-06 17:23:21');
INSERT INTO public.konubasvurulari VALUES (871, 384, '230202015', '0', 1, '2026-03-06 17:26:07');
INSERT INTO public.konubasvurulari VALUES (872, 422, '230202060', '0', 1, '2026-03-06 17:31:40');
INSERT INTO public.konubasvurulari VALUES (873, 422, '230202060', '230202087', 2, '2026-03-06 18:08:09');
INSERT INTO public.konubasvurulari VALUES (874, 400, '230202056', '0', 1, '2026-03-06 19:52:55');
INSERT INTO public.konubasvurulari VALUES (875, 413, '230201132', '0', 1, '2026-03-08 17:45:48');
INSERT INTO public.konubasvurulari VALUES (876, 457, '230201034', '230201098', 1, '2026-03-08 21:05:30');


--
-- Data for Name: mesajlar; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: ogrenciler; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.ogrenciler VALUES (22, '230202109', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (23, '230202023', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (24, '230202078', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (25, '220202076', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (26, '230202073', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (27, '230202103', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (28, '230202071', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (29, '230202101', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (30, '230202131', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (31, '230202012', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (32, '230202076', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (33, '230202126', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (34, '230202066', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (35, '230202095', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (36, '230202039', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (37, '230202097', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (38, '230202021', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (39, '230202061', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (40, '230202113', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (79, '240202004', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (80, '230202112', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (81, '230202010', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (82, '240202012', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (109, '230202046', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (110, '230202062', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (112, '230202045', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (113, '230202088', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (116, '230202037', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (117, '230202105', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (121, '230202068', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (125, '220202091', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (127, '230202001', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (128, '230202044', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (131, '230202058', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (132, '230202081', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (135, '230202083', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (136, '230202082', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (137, '230202070', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (138, '230202049', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (219, '240201300', 'ali yılmaz', 'Örgün', false, '4983ec114dac4138b54f61ed7c6e1ed0.png', '2026-04-06 13:42:55', 'scrypt:32768:8:1$Yt96A9iRyX9HSgcM$8466c82e92c1a2ab66ab89e0ddd4c412b2a0a8ea46d927921d486c2fb4d9e03e6211d16b59b4658b61040e445c1d611bf9c80f06e2ed466b2731ccdb4b029609', 3, 1);
INSERT INTO public.ogrenciler VALUES (139, '230202057', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (140, '230202036', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (143, '230202016', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (144, '230202035', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (148, '220202103', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (149, '240202005', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (150, '240202003', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (151, '220202040', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (152, '220202013', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (218, '3', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (220, '240201301', 'ahmet yılmaz', 'Örgün', false, '4109bc8954914bc3859a2ad14a9889a0.png', '2026-04-06 14:54:37', 'scrypt:32768:8:1$Yv8JP3jT8YYDkJwa$5a1e9d02f0094ed94cb7e637df4b8460fe90a23f4f3f7c67cd25e40642e7bcc82ad80d1e6d3574bf5ba5c66b9af77a9e94ca7f082db402be7726b65e7bda3772', 3, 1);
INSERT INTO public.ogrenciler VALUES (212, '230202122', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (118, '201230114', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (76, '210201049', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (106, '230201105', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (62, '230201107', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (145, '230201109', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (89, '230201111', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (58, '230201112', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (53, '230201117', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (92, '230201123', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (165, '230201131', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (209, '230201132', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (122, '230201139', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (77, '230201154', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (94, '240201119', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (98, '240201120', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (104, '240201122', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (146, '240201123', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (71, '240201124', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (5, '240201132', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (103, '250201110', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (1, '230202017', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (2, '230202026', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (3, '230202093', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (4, '230202050', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (7, '230202107', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (8, '230202043', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (9, '240202001', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (10, '230202084', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (11, '230202022', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (12, '230202091', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (13, '220202028', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (14, '230202064', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (15, '230202065', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (16, '230202108', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (17, '230202114', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (18, '230202048', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (19, '230202033', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (20, '230202013', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (21, '230202007', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (178, '230202060', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (179, '230202067', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (180, '230202052', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (181, '230202038', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (182, '230202080', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (183, '230202063', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (185, '230202018', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (186, '230202100', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (187, '230202029', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (188, '220202031', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (191, '230202040', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (192, '230202069', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (194, '230202104', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (195, '230202074', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (196, '230202086', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (203, '230202087', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (204, '230202015', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (206, '230202056', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (217, '230201057', 'Barışcan Özgen', 'Örgün', true, '9e0eecae152b436caa3d8833425363e2.png', '2026-04-02 11:21:03', 'scrypt:32768:8:1$rszyjRiDerGcM98P$4d96712b778d7f228b7b5383e046ca4c0ef43891b563bb5fdf0d5e8bad675e2f268676fe187d5d9653826ac2abab72062613b7abe37f5495f7eb0672197c1d2b', 1, 1);
INSERT INTO public.ogrenciler VALUES (153, '230202129', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (154, '230202047', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (213, '230201114', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (126, '230201029', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (214, '0', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (155, '230202075', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (156, '230202020', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (157, '220202053', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (158, '230202053', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (159, '220202017', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (163, '220202083', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (164, '230201130', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (167, '220202027', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (215, '230201009', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (46, '230201004', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (70, '220201087', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (74, '220201146', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (48, '230201020', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (50, '230201022', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (68, '230201023', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (49, '230201024', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (67, '230201027', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (123, '230201030', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (60, '230201031', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (124, '230201032', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (63, '230201033', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (65, '230201034', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (56, '230201037', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (114, '230201040', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (44, '230201041', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (91, '230201046', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (42, '230201048', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (96, '230201051', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (133, '230201053', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (72, '230201054', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (142, '230201055', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (64, '230201058', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (41, '230201061', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (90, '230201062', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (119, '230201065', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (51, '230201066', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (197, '230201067', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (141, '230201069', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (102, '230201070', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (115, '230201072', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (134, '230201073', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (108, '230201074', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (43, '230201075', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (97, '230201076', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (93, '230201078', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (100, '230201080', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (55, '230201081', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (59, '230201082', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (99, '230201085', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (57, '230201088', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (88, '230201090', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (87, '230201092', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (52, '230201093', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (6, '230201095', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (111, '230201097', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (66, '230201098', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (120, '230201099', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (95, '230201101', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (61, '230201102', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (105, '230201103', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (147, '230201104', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (198, '210201010', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (199, '210201037', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (201, '210201064', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (193, '210201083', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (101, '210201142', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (169, '220201006', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (85, '220201007', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (47, '220201028', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (83, '220201042', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (200, '220201043', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (78, '220201046', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (86, '220201050', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (84, '220201054', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (54, '220201068', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (170, '220201074', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (75, '220201075', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (166, '220201080', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (162, '220201082', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (107, '220201142', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (73, '220201144', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (161, '230201035', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (160, '230201049', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (173, '230201064', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (129, '230201087', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (130, '230201089', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (207, '230201071', NULL, 'Örgün', false, NULL, NULL, NULL, 1, 1);
INSERT INTO public.ogrenciler VALUES (177, '230202054', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (184, '210202049', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (189, '240202013', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (190, '230202079', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (202, '220202110', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (205, '220202085', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (208, '230202077', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (210, '230202030', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (211, '240202016', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (168, '210202051', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (171, '230202019', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (172, '230202031', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (174, '230202027', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (175, '230202111', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);
INSERT INTO public.ogrenciler VALUES (176, '210202045', NULL, 'Gece', false, NULL, NULL, NULL, 2, 1);


--
-- Data for Name: sorubasvurulari; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.sorubasvurulari VALUES (1183, 436, '230202111', '2026-03-18 09:24:01', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1132, 372, '220202076', '2026-03-12 14:22:20', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1134, 410, '230202030', '2026-03-12 14:42:05', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1136, 410, '230202113', '2026-03-12 14:49:45', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1144, 470, '230202075', '2026-03-12 20:56:42', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1146, 375, '220201050', '2026-03-13 11:04:56', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1150, 464, '210202064', '2026-03-13 14:30:39', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1153, 372, '240202003', '2026-03-13 18:07:39', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (619, 394, '230202043', '2026-03-03 22:06:06', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (622, 454, '230202107', '2026-03-03 22:08:27', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (631, 454, '230202043', '2026-03-03 22:51:33', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1176, 387, '210201131', '2026-03-29 19:37:23', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (636, 376, '230202010', '2026-03-03 22:57:29', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1177, 395, '210201131', '2026-03-29 19:37:48', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1178, 403, '210201131', '2026-03-29 19:38:47', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (696, 435, '230201102', '2026-03-04 00:27:17', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (712, 437, '240201124', '2026-03-04 00:36:56', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (714, 453, '240201124', '2026-03-04 00:37:59', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (716, 437, '230201054', '2026-03-04 00:39:35', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (721, 445, '230201117', '2026-03-04 00:42:02', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (727, 435, '220201087', '2026-03-04 00:45:57', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (729, 437, '220201007', '2026-03-04 00:47:29', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (734, 445, '220201087', '2026-03-04 00:48:28', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (738, 381, '210201049', '2026-03-04 00:49:40', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (741, 463, '220201007', '2026-03-04 00:50:15', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (745, 438, '230202122', '2026-03-04 00:53:17', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (793, 405, '240201120', '2026-03-04 01:50:46', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (796, 439, '210201142', '2026-03-04 01:57:50', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (799, 363, '210201142', '2026-03-04 01:58:18', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (803, 375, '230201070', '2026-03-04 02:04:19', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (804, 363, '230201070', '2026-03-04 02:04:55', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (812, 394, '230202046', '2026-03-04 10:56:23', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (822, 447, '230201055', '2026-03-04 11:48:29', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (827, 375, '230201154', '2026-03-04 12:08:19', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (834, 465, '230201154', '2026-03-04 12:21:42', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (846, 465, '230201085', '2026-03-04 12:36:53', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (847, 465, '230201080', '2026-03-04 12:42:41', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (848, 465, '230201074', '2026-03-04 12:45:19', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (849, 465, '220201142', '2026-03-04 12:50:32', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (866, 449, '230201080', '2026-03-04 13:29:01', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (867, 449, '230201074', '2026-03-04 13:29:22', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (868, 465, '230201087', '2026-03-04 13:30:15', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (869, 379, '230201087', '2026-03-04 13:30:43', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (870, 379, '230201089', '2026-03-04 13:30:48', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (871, 405, '230201087', '2026-03-04 13:32:16', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (872, 405, '230201089', '2026-03-04 13:32:17', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (873, 465, '230201089', '2026-03-04 13:32:56', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (901, 364, '230202036', '2026-03-04 14:42:22', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (914, 462, '230202108', '2026-03-04 15:22:19', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (933, 441, '220201144', '2026-03-04 22:15:43', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (936, 449, '230201069', '2026-03-04 22:38:31', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (937, 439, '230201069', '2026-03-04 22:39:24', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (941, 380, '230202027', '2026-03-04 23:30:58', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (942, 380, '230202053', '2026-03-04 23:31:11', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (946, 382, '230202054', '2026-03-04 23:46:51', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (949, 441, '230201034', '2026-03-04 23:49:19', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (951, 380, '230202047', '2026-03-05 00:08:39', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (960, 461, '230201098', '2026-03-05 01:12:49', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (961, 375, '230201098', '2026-03-05 01:13:20', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (962, 453, '220201144', '2026-03-05 06:46:57', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (965, 469, '230201112', '2026-03-05 10:18:58', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (966, 379, '220201144', '2026-03-05 11:03:48', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (967, 438, '230202080', '2026-03-05 11:36:30', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (971, 376, '230202038', '2026-03-05 11:39:05', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (977, 394, '210202049', '2026-03-05 13:25:35', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (978, 454, '210202049', '2026-03-05 13:26:30', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (979, 380, '210202049', '2026-03-05 13:27:22', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (993, 480, '220202017', '2026-03-05 15:07:19', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (996, 402, '230202061', '2026-03-05 15:14:18', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1000, 402, '230202021', '2026-03-05 15:22:16', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1003, 362, '240202013', '2026-03-05 15:28:52', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1005, 436, '240202013', '2026-03-05 15:29:17', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1006, 446, '240202013', '2026-03-05 15:30:43', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1015, 462, '230202079', '2026-03-05 16:41:54', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1022, 445, '230201064', '2026-03-05 22:28:44', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1023, 449, '230201064', '2026-03-05 22:29:04', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1024, 453, '230201064', '2026-03-05 22:29:15', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1049, 418, '220202085', '2026-03-06 00:08:04', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1053, 379, '230201023', '2026-03-06 00:51:19', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1058, 407, '230201105', '2026-03-06 01:04:50', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1063, 402, '230202063', '2026-03-06 02:26:36', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1064, 480, '230202063', '2026-03-06 02:27:30', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1066, 402, '230202129', '2026-03-06 02:29:59', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1067, 480, '230202129', '2026-03-06 02:30:21', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1071, 464, '220202083', '2026-03-06 11:04:12', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1072, 361, '230201139', '2026-03-06 11:14:06', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1082, 394, '230202037', '2026-03-06 15:09:25', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1085, 382, '230202068', '2026-03-06 16:05:00', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1086, 438, '230202068', '2026-03-06 16:05:53', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1087, 462, '230202068', '2026-03-06 16:06:21', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1094, 382, '230202101', '2026-03-06 17:13:10', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1112, 393, '230201132', '2026-03-08 17:12:10', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1113, 440, '230202077', '2026-03-08 17:40:02', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1114, 439, '230201055', '2026-03-08 17:40:12', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1115, 376, '230202077', '2026-03-08 17:41:01', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1121, 382, '240202016', '2026-03-09 23:54:12', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1126, 464, '230202007', '2026-03-10 19:26:36', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1181, 426, '230202071', '2026-03-13 19:30:14', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1182, 424, '230202019', '2026-03-22 16:20:10', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (615, 448, '230202065', '2026-03-03 21:47:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (616, 440, '230202126', '2026-03-03 21:48:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (617, 376, '220202103', '2026-03-03 22:00:53', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (618, 364, '220202103', '2026-03-03 22:02:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (620, 368, '230202043', '2026-03-03 22:06:31', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (621, 436, '230202107', '2026-03-03 22:07:31', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (623, 396, '230202043', '2026-03-03 22:09:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (624, 392, '230202107', '2026-03-03 22:10:24', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (625, 368, '230202107', '2026-03-03 22:41:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (626, 364, '230202093', '2026-03-03 22:45:21', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (627, 364, '230202050', '2026-03-03 22:45:25', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (628, 428, '230202050', '2026-03-03 22:48:28', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (629, 428, '230202093', '2026-03-03 22:48:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (630, 366, '230202039', '2026-03-03 22:50:49', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (632, 438, '230202093', '2026-03-03 22:51:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (633, 438, '230202050', '2026-03-03 22:51:46', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (634, 372, '230202039', '2026-03-03 22:55:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (635, 372, '230202010', '2026-03-03 22:56:29', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (637, 380, '230202039', '2026-03-03 22:58:09', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (638, 368, '230202010', '2026-03-03 22:59:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (639, 362, '230202010', '2026-03-03 23:00:01', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (640, 442, '230202010', '2026-03-03 23:00:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (641, 456, '230202010', '2026-03-03 23:06:57', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (642, 366, '230202097', '2026-03-03 23:08:40', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (643, 372, '230202097', '2026-03-03 23:08:58', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (644, 380, '230202097', '2026-03-03 23:09:15', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (645, 463, '230201066', '2026-03-04 00:05:47', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (646, 361, '220201028', '2026-03-04 00:08:53', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (647, 381, '230201081', '2026-03-04 00:09:34', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (648, 381, '220201068', '2026-03-04 00:09:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (649, 393, '230201081', '2026-03-04 00:11:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (650, 393, '220201068', '2026-03-04 00:11:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (651, 439, '230201066', '2026-03-04 00:11:08', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (652, 439, '230201022', '2026-03-04 00:12:24', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (653, 469, '230201020', '2026-03-04 00:12:26', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (654, 469, '230201020', '2026-03-04 00:12:57', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (655, 445, '230201020', '2026-03-04 00:13:28', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (656, 405, '220201068', '2026-03-04 00:13:29', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (657, 405, '230201081', '2026-03-04 00:13:31', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (658, 463, '230201024', '2026-03-04 00:13:48', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (659, 475, '230201020', '2026-03-04 00:14:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (660, 465, '230201066', '2026-03-04 00:15:02', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (661, 465, '230201022', '2026-03-04 00:15:03', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (662, 437, '230201031', '2026-03-04 00:17:10', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (663, 437, '230201082', '2026-03-04 00:17:34', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (664, 363, '220201087', '2026-03-04 00:18:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (665, 437, '230201061', '2026-03-04 00:18:24', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (666, 449, '230201020', '2026-03-04 00:18:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (667, 453, '230201061', '2026-03-04 00:19:30', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (668, 447, '230201048', '2026-03-04 00:19:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (669, 447, '230201033', '2026-03-04 00:19:36', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (670, 441, '230201037', '2026-03-04 00:19:40', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (671, 445, '230201031', '2026-03-04 00:19:50', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (672, 445, '230201082', '2026-03-04 00:19:50', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (673, 403, '230201109', '2026-03-04 00:20:12', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (674, 381, '230201037', '2026-03-04 00:20:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (675, 437, '230201033', '2026-03-04 00:20:53', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (676, 411, '230201037', '2026-03-04 00:21:03', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (677, 463, '230201075', '2026-03-04 00:21:56', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (678, 449, '230201066', '2026-03-04 00:22:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (679, 449, '230201024', '2026-03-04 00:22:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (680, 447, '230201109', '2026-03-04 00:22:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (681, 453, '230201082', '2026-03-04 00:22:18', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (682, 453, '230201031', '2026-03-04 00:22:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (683, 449, '230201022', '2026-03-04 00:22:26', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (684, 437, '230201058', '2026-03-04 00:24:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (685, 463, '230201041', '2026-03-04 00:24:40', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (686, 465, '230201041', '2026-03-04 00:25:02', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (687, 447, '230201058', '2026-03-04 00:25:03', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (688, 435, '230201048', '2026-03-04 00:25:18', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (689, 465, '230201075', '2026-03-04 00:25:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (690, 435, '230201109', '2026-03-04 00:26:09', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (691, 461, '230201033', '2026-03-04 00:26:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (692, 461, '230201048', '2026-03-04 00:26:24', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (693, 435, '230201061', '2026-03-04 00:26:34', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (694, 435, '230201107', '2026-03-04 00:26:52', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (695, 399, '230201057', '2026-03-04 00:26:56', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (697, 453, '230201107', '2026-03-04 00:28:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (698, 453, '230201102', '2026-03-04 00:28:12', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (699, 441, '230201088', '2026-03-04 00:28:29', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (700, 463, '230201107', '2026-03-04 00:29:08', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (701, 463, '230201102', '2026-03-04 00:29:15', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (702, 381, '230201088', '2026-03-04 00:29:30', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (703, 411, '230201088', '2026-03-04 00:29:50', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (704, 445, '230201093', '2026-03-04 00:29:57', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (705, 439, '230201057', '2026-03-04 00:30:32', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (706, 437, '230201093', '2026-03-04 00:30:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (707, 453, '230201093', '2026-03-04 00:32:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (708, 439, '230201075', '2026-03-04 00:32:48', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (709, 461, '230201058', '2026-03-04 00:33:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (710, 439, '230201041', '2026-03-04 00:34:09', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (711, 423, '230201057', '2026-03-04 00:35:08', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (713, 445, '240201124', '2026-03-04 00:37:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (715, 427, '230201024', '2026-03-04 00:38:29', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (717, 445, '230201054', '2026-03-04 00:40:05', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (718, 363, '230201117', '2026-03-04 00:40:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (719, 375, '230201117', '2026-03-04 00:41:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (720, 381, '230201009', '2026-03-04 00:41:26', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (722, 415, '220201075', '2026-03-04 00:42:50', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (723, 365, '220201042', '2026-03-04 00:43:18', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (724, 415, '210201049', '2026-03-04 00:43:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (725, 447, '230201054', '2026-03-04 00:44:20', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (726, 469, '220201087', '2026-03-04 00:45:34', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (728, 465, '230201004', '2026-03-04 00:47:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (730, 365, '220201007', '2026-03-04 00:47:56', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (731, 405, '230201078', '2026-03-04 00:48:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (732, 393, '220201042', '2026-03-04 00:48:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (733, 389, '220201046', '2026-03-04 00:48:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (735, 405, '230201061', '2026-03-04 00:48:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (736, 363, '230201004', '2026-03-04 00:48:48', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (737, 381, '220201075', '2026-03-04 00:48:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (739, 375, '220201042', '2026-03-04 00:49:46', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (740, 433, '230201102', '2026-03-04 00:49:49', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (742, 447, '230201097', '2026-03-04 00:50:18', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (743, 375, '230201004', '2026-03-04 00:50:40', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (744, 375, '220201146', '2026-03-04 00:50:45', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (746, 361, '220201042', '2026-03-04 00:53:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (747, 379, '230201078', '2026-03-04 00:53:55', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (748, 446, '230202122', '2026-03-04 00:56:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (749, 472, '230202122', '2026-03-04 00:56:29', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (750, 375, '220201075', '2026-03-04 00:56:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (751, 371, '230201078', '2026-03-04 00:56:40', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (752, 361, '220201054', '2026-03-04 00:57:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (753, 411, '220201054', '2026-03-04 00:58:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (754, 387, '220201054', '2026-03-04 01:01:03', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (755, 433, '230201046', '2026-03-04 01:01:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (756, 433, '230201123', '2026-03-04 01:01:50', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (757, 441, '230201090', '2026-03-04 01:02:53', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (758, 461, '230201123', '2026-03-04 01:04:55', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (759, 461, '230201046', '2026-03-04 01:05:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (760, 469, '220201146', '2026-03-04 01:05:27', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (761, 375, '210201049', '2026-03-04 01:08:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (762, 395, '230201090', '2026-03-04 01:08:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (763, 417, '230201046', '2026-03-04 01:10:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (764, 417, '230201123', '2026-03-04 01:11:23', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (765, 441, '220201146', '2026-03-04 01:11:24', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (766, 469, '230201090', '2026-03-04 01:16:31', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (767, 363, '230201020', '2026-03-04 01:16:48', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (768, 371, '240201119', '2026-03-04 01:17:08', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (769, 465, '230201101', '2026-03-04 01:17:54', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (770, 379, '240201119', '2026-03-04 01:18:12', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (771, 361, '240201119', '2026-03-04 01:20:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (772, 403, '230201101', '2026-03-04 01:21:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (773, 403, '230201020', '2026-03-04 01:22:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (774, 469, '230201101', '2026-03-04 01:23:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (775, 363, '220201050', '2026-03-04 01:25:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (776, 371, '210201049', '2026-03-04 01:25:54', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (777, 391, '230201092', '2026-03-04 01:26:58', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (778, 361, '220201050', '2026-03-04 01:28:45', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (779, 439, '220201050', '2026-03-04 01:31:28', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (780, 443, '230201076', '2026-03-04 01:31:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (781, 475, '220201007', '2026-03-04 01:36:57', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (782, 373, '220201050', '2026-03-04 01:38:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (783, 391, '230201090', '2026-03-04 01:39:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (784, 363, '230201111', '2026-03-04 01:43:13', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (785, 443, '240201120', '2026-03-04 01:44:23', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (786, 371, '230201111', '2026-03-04 01:45:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (787, 371, '230201062', '2026-03-04 01:45:12', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (788, 379, '230201111', '2026-03-04 01:45:54', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (789, 379, '230201062', '2026-03-04 01:46:00', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (790, 430, '230202074', '2026-03-04 01:46:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (791, 475, '230201092', '2026-03-04 01:46:27', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (792, 466, '230202074', '2026-03-04 01:49:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (794, 474, '230202074', '2026-03-04 01:51:34', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (795, 387, '230201062', '2026-03-04 01:56:20', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (797, 475, '240201120', '2026-03-04 01:57:55', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (798, 373, '210201142', '2026-03-04 01:58:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (800, 473, '230201076', '2026-03-04 01:59:21', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (801, 411, '230201092', '2026-03-04 02:02:13', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (802, 427, '230201070', '2026-03-04 02:04:01', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1025, 447, '230201049', '2026-03-05 22:37:12', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1026, 449, '230201049', '2026-03-05 22:37:27', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1029, 463, '230201064', '2026-03-05 22:42:28', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1031, 463, '230201049', '2026-03-05 22:42:54', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1032, 364, '230202086', '2026-03-05 22:48:19', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1040, 381, '230201027', '2026-03-05 23:45:16', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1041, 437, '230201027', '2026-03-05 23:45:51', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (1042, 463, '230201027', '2026-03-05 23:46:15', false, NULL);
INSERT INTO public.sorubasvurulari VALUES (805, 443, '250201110', '2026-03-04 02:11:46', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (806, 411, '230201076', '2026-03-04 02:13:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (807, 391, '240201122', '2026-03-04 02:13:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (808, 411, '240201122', '2026-03-04 02:14:52', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (809, 391, '250201110', '2026-03-04 02:15:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (810, 473, '240201122', '2026-03-04 02:17:23', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (811, 473, '250201110', '2026-03-04 02:21:09', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (813, 404, '230202062', '2026-03-04 10:59:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (814, 404, '230202046', '2026-03-04 11:00:49', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (815, 450, '230202062', '2026-03-04 11:02:29', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (816, 448, '230202062', '2026-03-04 11:09:00', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (817, 448, '230202046', '2026-03-04 11:09:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (818, 428, '230202045', '2026-03-04 11:19:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (819, 380, '230202045', '2026-03-04 11:19:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (820, 470, '230202045', '2026-03-04 11:23:02', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (821, 449, '230201055', '2026-03-04 11:47:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (823, 459, '230201055', '2026-03-04 11:49:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (824, 417, '230201040', '2026-03-04 11:56:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (825, 427, '230201040', '2026-03-04 11:58:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (826, 455, '230201040', '2026-03-04 11:59:05', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (828, 441, '230201154', '2026-03-04 12:08:40', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (829, 397, '230201114', '2026-03-04 12:11:10', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (830, 409, '230201114', '2026-03-04 12:12:23', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (831, 457, '230201114', '2026-03-04 12:13:31', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (832, 477, '230201085', '2026-03-04 12:14:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (833, 450, '230202065', '2026-03-04 12:20:26', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (835, 450, '230202064', '2026-03-04 12:22:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (836, 459, '230201065', '2026-03-04 12:23:08', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (837, 477, '230201080', '2026-03-04 12:23:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (838, 448, '230202070', '2026-03-04 12:24:27', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (839, 459, '230201099', '2026-03-04 12:24:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (840, 397, '230201099', '2026-03-04 12:26:00', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (841, 456, '230202070', '2026-03-04 12:26:34', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (842, 397, '230201065', '2026-03-04 12:27:09', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (843, 464, '230202070', '2026-03-04 12:27:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (844, 409, '230201099', '2026-03-04 12:28:32', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (845, 409, '230201065', '2026-03-04 12:28:34', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (850, 372, '240202012', '2026-03-04 12:50:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (851, 388, '240202012', '2026-03-04 12:51:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (852, 430, '240202012', '2026-03-04 12:51:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (853, 379, '220201142', '2026-03-04 13:05:24', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (854, 379, '230201074', '2026-03-04 13:08:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (855, 407, '230201085', '2026-03-04 13:15:20', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (856, 436, '230202001', '2026-03-04 13:15:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (583, 376, '230202026', '2026-03-03 17:44:03', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (584, 454, '240202001', '2026-03-03 18:41:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (585, 382, '220202028', '2026-03-03 18:42:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (586, 394, '220202028', '2026-03-03 18:42:25', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (587, 382, '240202001', '2026-03-03 18:42:26', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (588, 442, '220202028', '2026-03-03 18:42:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (589, 394, '230202095', '2026-03-03 18:42:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (590, 438, '240202001', '2026-03-03 18:42:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (591, 394, '230202066', '2026-03-03 18:43:15', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (592, 394, '230202103', '2026-03-03 18:43:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (593, 394, '230202073', '2026-03-03 18:45:21', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (594, 454, '230202084', '2026-03-03 18:46:21', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (595, 462, '230202084', '2026-03-03 18:46:49', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (596, 438, '230202084', '2026-03-03 18:47:15', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (597, 454, '230202048', '2026-03-03 18:53:34', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (598, 394, '230202048', '2026-03-03 18:56:55', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (599, 462, '230202048', '2026-03-03 18:57:40', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (600, 376, '230202033', '2026-03-03 19:00:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (601, 436, '230202103', '2026-03-03 19:00:58', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (602, 436, '230202095', '2026-03-03 19:01:56', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (603, 367, '230202071', '2026-03-03 19:03:58', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (604, 464, '230202071', '2026-03-03 19:04:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (605, 480, '230202071', '2026-03-03 19:04:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (606, 442, '230202033', '2026-03-03 19:05:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (857, 386, '230202001', '2026-03-04 13:15:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (858, 389, '220201142', '2026-03-04 13:15:58', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (859, 380, '230202001', '2026-03-04 13:16:28', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (860, 407, '230201074', '2026-03-04 13:19:20', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (861, 477, '230201032', '2026-03-04 13:22:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (862, 407, '220201142', '2026-03-04 13:23:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (863, 403, '230201032', '2026-03-04 13:26:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (864, 407, '230201080', '2026-03-04 13:26:52', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (865, 449, '230201085', '2026-03-04 13:28:09', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (874, 390, '230202001', '2026-03-04 13:34:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (875, 380, '230202058', '2026-03-04 13:35:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (876, 380, '230202081', '2026-03-04 13:35:23', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (877, 392, '230202058', '2026-03-04 13:41:30', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (878, 392, '230202081', '2026-03-04 13:42:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (879, 395, '230201032', '2026-03-04 13:46:25', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (880, 441, '230201030', '2026-03-04 13:50:21', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (881, 407, '230201053', '2026-03-04 13:50:49', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (882, 407, '230201073', '2026-03-04 13:51:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (883, 386, '230202058', '2026-03-04 13:53:52', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (884, 386, '230202081', '2026-03-04 13:54:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (885, 382, '230202083', '2026-03-04 14:01:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (886, 382, '230202082', '2026-03-04 14:01:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (887, 464, '230202057', '2026-03-04 14:07:41', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (888, 466, '230202057', '2026-03-04 14:08:10', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (889, 410, '230202083', '2026-03-04 14:08:20', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (890, 410, '230202082', '2026-03-04 14:08:42', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (891, 391, '230201080', '2026-03-04 14:11:50', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (892, 366, '230202057', '2026-03-04 14:13:23', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (893, 387, '230201053', '2026-03-04 14:13:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (894, 387, '230201073', '2026-03-04 14:13:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (895, 382, '230202057', '2026-03-04 14:14:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (896, 464, '230202036', '2026-03-04 14:29:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (897, 382, '230202036', '2026-03-04 14:39:09', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (898, 433, '230201073', '2026-03-04 14:39:55', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (899, 433, '230201053', '2026-03-04 14:40:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (900, 404, '230202036', '2026-03-04 14:41:55', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (902, 464, '230202035', '2026-03-04 14:43:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (903, 406, '230202035', '2026-03-04 14:44:27', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (904, 368, '230202035', '2026-03-04 14:50:01', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (905, 430, '230202062', '2026-03-04 14:51:34', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (906, 442, '230202016', '2026-03-04 14:59:28', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (907, 462, '230202016', '2026-03-04 15:07:56', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (908, 472, '230202016', '2026-03-04 15:13:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (909, 446, '230202078', '2026-03-04 15:19:57', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (910, 422, '230202023', '2026-03-04 15:20:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (911, 452, '230202078', '2026-03-04 15:21:01', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (912, 468, '230202023', '2026-03-04 15:21:26', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (913, 452, '230202114', '2026-03-04 15:21:57', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (915, 369, '3', '2026-03-04 15:29:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (916, 395, '240201123', '2026-03-04 16:07:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (917, 415, '240201123', '2026-03-04 16:07:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (918, 451, '240201123', '2026-03-04 16:08:05', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (919, 395, '230201104', '2026-03-04 16:08:26', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (920, 415, '230201104', '2026-03-04 16:08:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (921, 451, '230201104', '2026-03-04 16:08:53', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (922, 440, '230202131', '2026-03-04 16:15:56', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (923, 418, '220202103', '2026-03-04 16:30:47', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (924, 423, '230201009', '2026-03-04 18:14:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (925, 424, '230202083', '2026-03-04 21:07:05', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (926, 424, '230202082', '2026-03-04 21:07:26', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (927, 361, '220201006', '2026-03-04 21:12:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (928, 365, '220201074', '2026-03-04 21:12:31', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (929, 391, '220201074', '2026-03-04 21:14:00', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (930, 369, '220201006', '2026-03-04 21:14:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (931, 377, '220201006', '2026-03-04 21:14:41', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (932, 377, '220201074', '2026-03-04 21:15:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (934, 440, '230202044', '2026-03-04 22:28:47', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (935, 390, '230202044', '2026-03-04 22:31:54', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (938, 459, '230201069', '2026-03-04 22:39:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (939, 446, '230202027', '2026-03-04 23:30:10', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (940, 446, '230202053', '2026-03-04 23:30:27', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (943, 442, '230202027', '2026-03-04 23:31:47', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (944, 442, '230202053', '2026-03-04 23:32:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (945, 392, '230202054', '2026-03-04 23:46:23', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (947, 362, '230202054', '2026-03-04 23:47:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (948, 451, '230201034', '2026-03-04 23:47:49', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (950, 461, '230201034', '2026-03-04 23:50:55', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (952, 440, '230202021', '2026-03-05 00:49:21', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (953, 480, '230202060', '2026-03-05 00:59:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (954, 418, '230202060', '2026-03-05 01:01:21', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (955, 430, '230202060', '2026-03-05 01:02:13', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (956, 448, '230202052', '2026-03-05 01:05:21', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (957, 456, '230202052', '2026-03-05 01:05:45', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (958, 450, '230202052', '2026-03-05 01:06:02', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (959, 451, '230201098', '2026-03-05 01:12:00', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (963, 397, '230201112', '2026-03-05 10:07:47', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (964, 475, '230201112', '2026-03-05 10:15:41', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (968, 472, '230202080', '2026-03-05 11:36:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (969, 362, '230202080', '2026-03-05 11:37:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (970, 368, '230202038', '2026-03-05 11:37:52', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (972, 472, '230202038', '2026-03-05 11:47:32', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (973, 362, '220202091', '2026-03-05 11:52:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (974, 406, '220202091', '2026-03-05 11:55:12', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (975, 474, '220202091', '2026-03-05 11:58:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (976, 475, '230201117', '2026-03-05 13:23:49', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (980, 472, '230202088', '2026-03-05 13:53:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (981, 402, '230202018', '2026-03-05 13:56:18', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (982, 480, '230202018', '2026-03-05 13:58:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (983, 480, '230202100', '2026-03-05 13:58:45', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (984, 480, '230202088', '2026-03-05 13:59:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (985, 402, '230202029', '2026-03-05 14:01:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (986, 402, '230202029', '2026-03-05 14:01:20', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (987, 402, '230202100', '2026-03-05 14:01:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (988, 472, '230202029', '2026-03-05 14:01:44', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (989, 414, '220202085', '2026-03-05 14:54:42', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (577, 393, '230201095', '2026-03-03 17:29:53', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (578, 364, '230202108', '2026-03-03 17:33:08', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (579, 364, '230202114', '2026-03-03 17:35:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (580, 438, '230202017', '2026-03-03 17:38:15', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (581, 376, '230202017', '2026-03-03 17:40:28', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (582, 438, '230202026', '2026-03-03 17:43:03', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1027, 451, '230201049', '2026-03-05 22:37:40', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1028, 455, '230201064', '2026-03-05 22:40:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1030, 455, '230201049', '2026-03-05 22:42:41', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1033, 474, '230202086', '2026-03-05 22:49:31', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1034, 476, '230202086', '2026-03-05 22:49:56', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1035, 418, '230202044', '2026-03-05 22:51:42', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1036, 457, '240201120', '2026-03-05 23:01:15', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1037, 398, '230202031', '2026-03-05 23:31:28', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1038, 406, '230202031', '2026-03-05 23:32:10', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1039, 470, '230202031', '2026-03-05 23:33:58', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1127, 372, '230201130', '2026-03-11 10:11:48', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1128, 396, '230201130', '2026-03-11 10:18:30', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1129, 368, '220202027', '2026-03-11 12:49:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1130, 366, '240202003', '2026-03-11 20:18:23', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1131, 370, '220202076', '2026-03-12 14:19:45', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1133, 386, '230202030', '2026-03-12 14:40:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1135, 386, '230202113', '2026-03-12 14:49:13', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1137, 399, '230201072', '2026-03-12 16:15:47', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1138, 427, '230201072', '2026-03-12 16:19:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1139, 477, '230201072', '2026-03-12 16:21:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1140, 401, '220201050', '2026-03-12 16:22:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1141, 421, '230201029', '2026-03-12 16:43:24', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1142, 478, '230202075', '2026-03-12 20:55:49', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1143, 420, '230202075', '2026-03-12 20:56:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1145, 365, '230201132', '2026-03-13 11:01:32', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1147, 369, '230201132', '2026-03-13 11:24:50', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1148, 374, '230202091', '2026-03-13 14:02:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1149, 474, '210202064', '2026-03-13 14:14:10', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1151, 466, '210202064', '2026-03-13 14:38:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1152, 370, '240202003', '2026-03-13 17:16:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1154, 422, '230202040', '2026-03-15 20:49:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1155, 398, '230202040', '2026-03-15 22:23:45', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1156, 430, '230202040', '2026-03-15 23:25:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1157, 378, '220202027', '2026-03-17 23:19:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1158, 432, '230202111', '2026-03-18 09:38:30', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1159, 466, '230202111', '2026-03-18 10:15:09', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1160, 408, '230202037', '2026-03-21 12:07:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1161, 458, '230202037', '2026-03-21 12:08:01', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1162, 452, '230202019', '2026-03-22 16:16:10', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1163, 428, '230202019', '2026-03-22 16:17:56', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1164, 378, '240202005', '2026-03-24 17:46:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1165, 396, '240202005', '2026-03-24 17:58:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1166, 385, '220201006', '2026-03-24 22:00:26', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1167, 409, '220201006', '2026-03-24 22:06:12', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1168, 443, '230201035', '2026-03-26 16:33:47', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1169, 477, '230201035', '2026-03-26 16:38:27', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1170, 431, '230201035', '2026-03-26 16:40:09', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1171, 377, '230201067', '2026-03-27 02:08:00', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1172, 384, '230202013', '2026-03-27 16:09:30', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1173, 384, '230202015', '2026-03-27 17:23:15', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1174, 378, '240202003', '2026-03-27 17:53:08', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1175, 370, '240202005', '2026-03-27 18:10:55', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1179, 366, '230202104', '2026-04-01 18:07:58', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1180, 389, '230201029', '2026-04-02 14:14:20', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (607, 454, '230202101', '2026-03-03 19:07:01', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (608, 452, '230202101', '2026-03-03 19:07:30', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (609, 462, '230202101', '2026-03-03 19:07:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (610, 364, '230202033', '2026-03-03 19:13:49', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (611, 436, '230202073', '2026-03-03 19:25:13', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (612, 436, '230202066', '2026-03-03 19:30:18', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (613, 448, '230202064', '2026-03-03 21:47:03', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (614, 440, '230202076', '2026-03-03 21:47:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1017, 416, '230202109', '2026-03-05 16:54:00', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1018, 426, '230202101', '2026-03-05 17:07:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1019, 460, '220202085', '2026-03-05 17:15:08', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1020, 418, '230202064', '2026-03-05 21:47:35', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1021, 418, '230202065', '2026-03-05 21:47:39', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1043, 455, '230201030', '2026-03-05 23:54:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1044, 417, '230201023', '2026-03-05 23:54:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1045, 389, '230201030', '2026-03-05 23:56:42', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1046, 395, '230201023', '2026-03-05 23:56:58', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1047, 393, '230201097', '2026-03-05 23:58:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1048, 477, '230201101', '2026-03-06 00:04:45', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1050, 403, '230201051', '2026-03-06 00:32:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1051, 377, '230201105', '2026-03-06 00:46:15', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1052, 421, '230201051', '2026-03-06 00:49:13', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1054, 372, '220202083', '2026-03-06 00:51:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1055, 396, '220202083', '2026-03-06 00:52:18', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1056, 387, '230201105', '2026-03-06 00:53:12', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1057, 471, '230201051', '2026-03-06 00:53:23', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1059, 425, '230201075', '2026-03-06 01:07:30', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1060, 425, '230201041', '2026-03-06 01:08:02', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1061, 467, '220201075', '2026-03-06 01:10:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1062, 425, '230201105', '2026-03-06 01:32:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1065, 414, '230202063', '2026-03-06 02:28:08', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1068, 414, '230202129', '2026-03-06 02:30:52', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1069, 395, '220201043', '2026-03-06 05:38:48', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1070, 403, '220201043', '2026-03-06 05:41:54', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1073, 387, '230201067', '2026-03-06 11:21:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1074, 450, '230202013', '2026-03-06 12:23:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1075, 460, '230202131', '2026-03-06 12:43:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1076, 396, '230202112', '2026-03-06 13:01:25', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1077, 378, '230202112', '2026-03-06 13:03:20', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1078, 410, '230202112', '2026-03-06 13:15:43', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1079, 410, '240202004', '2026-03-06 13:16:29', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1080, 404, '230202057', '2026-03-06 13:19:32', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1081, 468, '230202131', '2026-03-06 13:38:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1083, 406, '230202067', '2026-03-06 15:53:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1084, 458, '230202067', '2026-03-06 15:56:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1088, 389, '210201083', '2026-03-06 16:07:58', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1089, 409, '210201083', '2026-03-06 16:12:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1090, 473, '210201083', '2026-03-06 16:14:28', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1091, 410, '230202071', '2026-03-06 17:10:54', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1092, 410, '230202101', '2026-03-06 17:11:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1093, 452, '230202068', '2026-03-06 17:12:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1095, 416, '220202110', '2026-03-06 17:21:22', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1096, 428, '220202110', '2026-03-06 17:22:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1097, 468, '220202110', '2026-03-06 17:26:14', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1098, 404, '230202013', '2026-03-06 17:45:02', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1099, 452, '230202109', '2026-03-06 17:50:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1100, 470, '230202076', '2026-03-06 19:01:32', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1101, 470, '230202126', '2026-03-06 19:01:46', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1102, 459, '240201120', '2026-03-06 20:59:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1103, 471, '230201103', '2026-03-06 21:29:18', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1104, 443, '230201103', '2026-03-06 21:39:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1105, 427, '230201103', '2026-03-06 21:52:32', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1106, 456, '230202076', '2026-03-07 13:42:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1107, 456, '230202126', '2026-03-07 13:42:34', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1108, 470, '230202067', '2026-03-07 23:17:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1109, 467, '230201112', '2026-03-08 04:04:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1110, 385, '230201132', '2026-03-08 17:10:58', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1111, 367, '230201132', '2026-03-08 17:11:30', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1116, 459, '230201055', '2026-03-08 17:42:11', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1117, 444, '230202077', '2026-03-08 17:42:20', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1118, 423, '210201064', '2026-03-09 17:03:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1119, 429, '210201064', '2026-03-09 17:04:31', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1120, 467, '210201064', '2026-03-09 17:07:54', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1122, 399, '230201131', '2026-03-10 01:27:21', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1123, 415, '230201131', '2026-03-10 01:30:03', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1124, 451, '230201131', '2026-03-10 01:33:56', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1125, 389, '230201009', '2026-03-10 18:00:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (564, 462, '230202066', '2026-03-03 16:53:19', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (565, 462, '230202095', '2026-03-03 16:53:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (566, 454, '230202103', '2026-03-03 16:54:37', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (567, 454, '230202073', '2026-03-03 16:54:57', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (568, 374, '230202078', '2026-03-03 16:55:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (569, 374, '230202023', '2026-03-03 16:55:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (570, 405, '230201095', '2026-03-03 17:18:10', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (571, 405, '240201132', '2026-03-03 17:18:41', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (572, 376, '230202114', '2026-03-03 17:24:40', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (573, 376, '230202108', '2026-03-03 17:27:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (574, 435, '230201095', '2026-03-03 17:28:04', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (575, 435, '240201132', '2026-03-03 17:29:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (576, 393, '240201132', '2026-03-03 17:29:51', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (990, 396, '240202004', '2026-03-05 15:04:12', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (991, 378, '240202004', '2026-03-05 15:04:44', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (992, 480, '220202031', '2026-03-05 15:07:17', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (994, 402, '220202017', '2026-03-05 15:08:33', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (995, 402, '220202031', '2026-03-05 15:08:45', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (997, 446, '220202017', '2026-03-05 15:15:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (998, 446, '220202031', '2026-03-05 15:15:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (999, 362, '230202021', '2026-03-05 15:20:31', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1001, 464, '230202088', '2026-03-05 15:22:40', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1002, 362, '230202061', '2026-03-05 15:25:09', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1004, 440, '230202061', '2026-03-05 15:29:06', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1007, 418, '230202018', '2026-03-05 15:34:16', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1008, 414, '230202047', '2026-03-05 15:39:38', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1009, 374, '230202022', '2026-03-05 16:14:57', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1010, 412, '230202022', '2026-03-05 16:18:07', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1011, 374, '230202114', '2026-03-05 16:19:36', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1012, 374, '230202108', '2026-03-05 16:19:59', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1013, 470, '230202079', '2026-03-05 16:38:02', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1014, 460, '230202079', '2026-03-05 16:41:20', true, NULL);
INSERT INTO public.sorubasvurulari VALUES (1016, 460, '230202109', '2026-03-05 16:48:41', true, NULL);


--
-- Data for Name: sorukontrolculeri; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.sorukontrolculeri VALUES (1, '230201057', 'scrypt:32768:8:1$x6MKMK5Zlr9xfG5F$939aaac8c6f9720c171d3e1e907cb38c6efada52497b971368758942d69c384d5f21ffc17f0c9b4d7c2e2e49a9f54d3726cd1f18b42813321a7d231743891244', 'Barışcan Özgen', true, 1);


--
-- Data for Name: sunumgorevlileri; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.sunumgorevlileri VALUES (318, 362, 11);
INSERT INTO public.sunumgorevlileri VALUES (319, 362, 12);
INSERT INTO public.sunumgorevlileri VALUES (320, 364, 116);
INSERT INTO public.sunumgorevlileri VALUES (321, 364, 117);
INSERT INTO public.sunumgorevlileri VALUES (322, 366, 125);
INSERT INTO public.sunumgorevlileri VALUES (323, 368, 36);
INSERT INTO public.sunumgorevlileri VALUES (324, 368, 37);
INSERT INTO public.sunumgorevlileri VALUES (325, 370, 40);
INSERT INTO public.sunumgorevlileri VALUES (326, 372, 79);
INSERT INTO public.sunumgorevlileri VALUES (327, 372, 80);
INSERT INTO public.sunumgorevlileri VALUES (328, 374, 1);
INSERT INTO public.sunumgorevlileri VALUES (329, 374, 2);
INSERT INTO public.sunumgorevlileri VALUES (330, 376, 23);
INSERT INTO public.sunumgorevlileri VALUES (331, 376, 24);
INSERT INTO public.sunumgorevlileri VALUES (332, 378, 163);
INSERT INTO public.sunumgorevlileri VALUES (333, 378, 164);
INSERT INTO public.sunumgorevlileri VALUES (334, 380, 127);
INSERT INTO public.sunumgorevlileri VALUES (335, 380, 128);
INSERT INTO public.sunumgorevlileri VALUES (336, 382, 7);
INSERT INTO public.sunumgorevlileri VALUES (337, 382, 8);
INSERT INTO public.sunumgorevlileri VALUES (338, 384, 204);
INSERT INTO public.sunumgorevlileri VALUES (339, 386, 3);
INSERT INTO public.sunumgorevlileri VALUES (340, 386, 4);
INSERT INTO public.sunumgorevlileri VALUES (341, 388, 153);
INSERT INTO public.sunumgorevlileri VALUES (342, 388, 154);
INSERT INTO public.sunumgorevlileri VALUES (343, 390, 131);
INSERT INTO public.sunumgorevlileri VALUES (344, 390, 132);
INSERT INTO public.sunumgorevlileri VALUES (345, 392, 167);
INSERT INTO public.sunumgorevlileri VALUES (346, 392, 168);
INSERT INTO public.sunumgorevlileri VALUES (347, 394, 9);
INSERT INTO public.sunumgorevlileri VALUES (348, 394, 10);
INSERT INTO public.sunumgorevlileri VALUES (349, 396, 81);
INSERT INTO public.sunumgorevlileri VALUES (350, 396, 82);
INSERT INTO public.sunumgorevlileri VALUES (351, 398, 137);
INSERT INTO public.sunumgorevlileri VALUES (352, 398, 138);
INSERT INTO public.sunumgorevlileri VALUES (353, 400, 206);
INSERT INTO public.sunumgorevlileri VALUES (354, 402, 112);
INSERT INTO public.sunumgorevlileri VALUES (355, 402, 113);
INSERT INTO public.sunumgorevlileri VALUES (356, 404, 143);
INSERT INTO public.sunumgorevlileri VALUES (357, 404, 144);
INSERT INTO public.sunumgorevlileri VALUES (358, 406, 25);
INSERT INTO public.sunumgorevlileri VALUES (359, 406, 25);
INSERT INTO public.sunumgorevlileri VALUES (360, 408, 171);
INSERT INTO public.sunumgorevlileri VALUES (361, 408, 172);
INSERT INTO public.sunumgorevlileri VALUES (362, 410, 121);
INSERT INTO public.sunumgorevlileri VALUES (363, 410, 121);
INSERT INTO public.sunumgorevlileri VALUES (364, 412, 148);
INSERT INTO public.sunumgorevlileri VALUES (365, 414, 188);
INSERT INTO public.sunumgorevlileri VALUES (366, 414, 159);
INSERT INTO public.sunumgorevlileri VALUES (367, 416, 151);
INSERT INTO public.sunumgorevlileri VALUES (368, 416, 152);
INSERT INTO public.sunumgorevlileri VALUES (369, 418, 20);
INSERT INTO public.sunumgorevlileri VALUES (370, 418, 21);
INSERT INTO public.sunumgorevlileri VALUES (371, 420, 182);
INSERT INTO public.sunumgorevlileri VALUES (372, 420, 181);
INSERT INTO public.sunumgorevlileri VALUES (373, 422, 178);
INSERT INTO public.sunumgorevlileri VALUES (374, 424, 191);
INSERT INTO public.sunumgorevlileri VALUES (375, 424, 192);
INSERT INTO public.sunumgorevlileri VALUES (376, 426, 135);
INSERT INTO public.sunumgorevlileri VALUES (377, 426, 136);
INSERT INTO public.sunumgorevlileri VALUES (378, 428, 109);
INSERT INTO public.sunumgorevlileri VALUES (379, 428, 110);
INSERT INTO public.sunumgorevlileri VALUES (380, 430, 10);
INSERT INTO public.sunumgorevlileri VALUES (381, 430, 12);
INSERT INTO public.sunumgorevlileri VALUES (382, 432, 203);
INSERT INTO public.sunumgorevlileri VALUES (383, 432, 194);
INSERT INTO public.sunumgorevlileri VALUES (384, 434, 155);
INSERT INTO public.sunumgorevlileri VALUES (385, 434, 156);
INSERT INTO public.sunumgorevlileri VALUES (386, 436, 18);
INSERT INTO public.sunumgorevlileri VALUES (387, 436, 19);
INSERT INTO public.sunumgorevlileri VALUES (388, 438, 16);
INSERT INTO public.sunumgorevlileri VALUES (389, 438, 17);
INSERT INTO public.sunumgorevlileri VALUES (390, 440, 14);
INSERT INTO public.sunumgorevlileri VALUES (391, 440, 15);
INSERT INTO public.sunumgorevlileri VALUES (392, 442, 13);
INSERT INTO public.sunumgorevlileri VALUES (393, 442, 13);
INSERT INTO public.sunumgorevlileri VALUES (394, 444, 149);
INSERT INTO public.sunumgorevlileri VALUES (395, 444, 150);
INSERT INTO public.sunumgorevlileri VALUES (396, 446, 80);
INSERT INTO public.sunumgorevlileri VALUES (397, 446, 157);
INSERT INTO public.sunumgorevlileri VALUES (398, 448, 32);
INSERT INTO public.sunumgorevlileri VALUES (399, 448, 33);
INSERT INTO public.sunumgorevlileri VALUES (400, 450, 30);
INSERT INTO public.sunumgorevlileri VALUES (401, 450, 31);
INSERT INTO public.sunumgorevlileri VALUES (402, 452, 28);
INSERT INTO public.sunumgorevlileri VALUES (403, 452, 29);
INSERT INTO public.sunumgorevlileri VALUES (404, 454, 34);
INSERT INTO public.sunumgorevlileri VALUES (405, 454, 35);
INSERT INTO public.sunumgorevlileri VALUES (406, 456, 175);
INSERT INTO public.sunumgorevlileri VALUES (407, 456, 176);
INSERT INTO public.sunumgorevlileri VALUES (408, 458, 195);
INSERT INTO public.sunumgorevlileri VALUES (409, 458, 196);
INSERT INTO public.sunumgorevlileri VALUES (410, 460, 183);
INSERT INTO public.sunumgorevlileri VALUES (411, 460, 153);
INSERT INTO public.sunumgorevlileri VALUES (412, 462, 26);
INSERT INTO public.sunumgorevlileri VALUES (413, 462, 27);
INSERT INTO public.sunumgorevlileri VALUES (414, 464, 38);
INSERT INTO public.sunumgorevlileri VALUES (415, 464, 39);
INSERT INTO public.sunumgorevlileri VALUES (416, 466, 139);
INSERT INTO public.sunumgorevlileri VALUES (417, 466, 140);
INSERT INTO public.sunumgorevlileri VALUES (418, 468, 159);
INSERT INTO public.sunumgorevlileri VALUES (419, 468, 151);
INSERT INTO public.sunumgorevlileri VALUES (420, 470, 22);
INSERT INTO public.sunumgorevlileri VALUES (421, 470, 22);
INSERT INTO public.sunumgorevlileri VALUES (422, 472, 185);
INSERT INTO public.sunumgorevlileri VALUES (423, 472, 186);
INSERT INTO public.sunumgorevlileri VALUES (424, 474, 117);
INSERT INTO public.sunumgorevlileri VALUES (425, 474, 158);
INSERT INTO public.sunumgorevlileri VALUES (426, 476, 179);
INSERT INTO public.sunumgorevlileri VALUES (427, 476, 180);
INSERT INTO public.sunumgorevlileri VALUES (428, 478, 174);
INSERT INTO public.sunumgorevlileri VALUES (429, 478, 158);
INSERT INTO public.sunumgorevlileri VALUES (430, 480, 187);
INSERT INTO public.sunumgorevlileri VALUES (431, 361, 101);
INSERT INTO public.sunumgorevlileri VALUES (432, 361, 102);
INSERT INTO public.sunumgorevlileri VALUES (433, 363, 58);
INSERT INTO public.sunumgorevlileri VALUES (434, 365, 75);
INSERT INTO public.sunumgorevlileri VALUES (435, 365, 76);
INSERT INTO public.sunumgorevlileri VALUES (436, 367, 89);
INSERT INTO public.sunumgorevlileri VALUES (437, 367, 90);
INSERT INTO public.sunumgorevlileri VALUES (438, 369, 47);
INSERT INTO public.sunumgorevlileri VALUES (439, 369, 47);
INSERT INTO public.sunumgorevlileri VALUES (440, 371, 73);
INSERT INTO public.sunumgorevlileri VALUES (441, 371, 74);
INSERT INTO public.sunumgorevlileri VALUES (442, 373, 98);
INSERT INTO public.sunumgorevlileri VALUES (443, 373, 160);
INSERT INTO public.sunumgorevlileri VALUES (444, 375, 56);
INSERT INTO public.sunumgorevlileri VALUES (445, 375, 57);
INSERT INTO public.sunumgorevlileri VALUES (446, 377, 67);
INSERT INTO public.sunumgorevlileri VALUES (447, 377, 68);
INSERT INTO public.sunumgorevlileri VALUES (448, 379, 105);
INSERT INTO public.sunumgorevlileri VALUES (449, 379, 106);
INSERT INTO public.sunumgorevlileri VALUES (450, 381, 5);
INSERT INTO public.sunumgorevlileri VALUES (451, 381, 6);
INSERT INTO public.sunumgorevlileri VALUES (452, 383, 76);
INSERT INTO public.sunumgorevlileri VALUES (453, 383, 75);
INSERT INTO public.sunumgorevlileri VALUES (454, 385, 161);
INSERT INTO public.sunumgorevlileri VALUES (455, 385, 68);
INSERT INTO public.sunumgorevlileri VALUES (456, 387, 93);
INSERT INTO public.sunumgorevlileri VALUES (457, 387, 94);
INSERT INTO public.sunumgorevlileri VALUES (458, 389, 217);
INSERT INTO public.sunumgorevlileri VALUES (459, 389, 70);
INSERT INTO public.sunumgorevlileri VALUES (460, 391, 97);
INSERT INTO public.sunumgorevlileri VALUES (461, 391, 98);
INSERT INTO public.sunumgorevlileri VALUES (462, 393, 119);
INSERT INTO public.sunumgorevlileri VALUES (463, 393, 120);
INSERT INTO public.sunumgorevlileri VALUES (464, 395, 85);
INSERT INTO public.sunumgorevlileri VALUES (465, 395, 86);
INSERT INTO public.sunumgorevlileri VALUES (466, 397, 72);
INSERT INTO public.sunumgorevlileri VALUES (467, 397, 166);
INSERT INTO public.sunumgorevlileri VALUES (468, 399, 193);
INSERT INTO public.sunumgorevlileri VALUES (469, 399, 201);
INSERT INTO public.sunumgorevlileri VALUES (470, 401, 122);
INSERT INTO public.sunumgorevlileri VALUES (471, 401, 122);
INSERT INTO public.sunumgorevlileri VALUES (472, 403, 215);
INSERT INTO public.sunumgorevlileri VALUES (473, 403, 46);
INSERT INTO public.sunumgorevlileri VALUES (474, 405, 200);
INSERT INTO public.sunumgorevlileri VALUES (475, 405, 162);
INSERT INTO public.sunumgorevlileri VALUES (476, 407, 123);
INSERT INTO public.sunumgorevlileri VALUES (477, 407, 124);
INSERT INTO public.sunumgorevlileri VALUES (478, 411, 114);
INSERT INTO public.sunumgorevlileri VALUES (479, 411, 115);
INSERT INTO public.sunumgorevlileri VALUES (480, 413, 209);
INSERT INTO public.sunumgorevlileri VALUES (481, 415, 83);
INSERT INTO public.sunumgorevlileri VALUES (482, 415, 84);
INSERT INTO public.sunumgorevlileri VALUES (483, 417, 162);
INSERT INTO public.sunumgorevlileri VALUES (484, 417, 160);
INSERT INTO public.sunumgorevlileri VALUES (485, 421, 165);
INSERT INTO public.sunumgorevlileri VALUES (486, 421, 98);
INSERT INTO public.sunumgorevlileri VALUES (487, 423, 145);
INSERT INTO public.sunumgorevlileri VALUES (488, 425, 169);
INSERT INTO public.sunumgorevlileri VALUES (489, 425, 170);
INSERT INTO public.sunumgorevlileri VALUES (490, 427, 91);
INSERT INTO public.sunumgorevlileri VALUES (491, 427, 92);
INSERT INTO public.sunumgorevlileri VALUES (492, 431, 95);
INSERT INTO public.sunumgorevlileri VALUES (493, 431, 96);
INSERT INTO public.sunumgorevlileri VALUES (494, 435, 52);
INSERT INTO public.sunumgorevlileri VALUES (495, 435, 53);
INSERT INTO public.sunumgorevlileri VALUES (496, 437, 54);
INSERT INTO public.sunumgorevlileri VALUES (497, 437, 55);
INSERT INTO public.sunumgorevlileri VALUES (498, 439, 61);
INSERT INTO public.sunumgorevlileri VALUES (499, 439, 62);
INSERT INTO public.sunumgorevlileri VALUES (500, 441, 133);
INSERT INTO public.sunumgorevlileri VALUES (501, 441, 134);
INSERT INTO public.sunumgorevlileri VALUES (502, 443, 87);
INSERT INTO public.sunumgorevlileri VALUES (503, 443, 88);
INSERT INTO public.sunumgorevlileri VALUES (504, 445, 41);
INSERT INTO public.sunumgorevlileri VALUES (505, 445, 42);
INSERT INTO public.sunumgorevlileri VALUES (506, 447, 59);
INSERT INTO public.sunumgorevlileri VALUES (507, 447, 60);
INSERT INTO public.sunumgorevlileri VALUES (508, 449, 43);
INSERT INTO public.sunumgorevlileri VALUES (509, 449, 44);
INSERT INTO public.sunumgorevlileri VALUES (510, 451, 141);
INSERT INTO public.sunumgorevlileri VALUES (511, 451, 142);
INSERT INTO public.sunumgorevlileri VALUES (512, 453, 63);
INSERT INTO public.sunumgorevlileri VALUES (513, 453, 64);
INSERT INTO public.sunumgorevlileri VALUES (514, 455, 146);
INSERT INTO public.sunumgorevlileri VALUES (515, 455, 147);
INSERT INTO public.sunumgorevlileri VALUES (516, 457, 65);
INSERT INTO public.sunumgorevlileri VALUES (517, 457, 66);
INSERT INTO public.sunumgorevlileri VALUES (518, 459, 111);
INSERT INTO public.sunumgorevlileri VALUES (519, 459, 118);
INSERT INTO public.sunumgorevlileri VALUES (520, 461, 71);
INSERT INTO public.sunumgorevlileri VALUES (521, 461, 72);
INSERT INTO public.sunumgorevlileri VALUES (522, 463, 50);
INSERT INTO public.sunumgorevlileri VALUES (523, 463, 51);
INSERT INTO public.sunumgorevlileri VALUES (524, 465, 48);
INSERT INTO public.sunumgorevlileri VALUES (525, 465, 49);
INSERT INTO public.sunumgorevlileri VALUES (526, 467, 103);
INSERT INTO public.sunumgorevlileri VALUES (527, 467, 104);
INSERT INTO public.sunumgorevlileri VALUES (528, 469, 99);
INSERT INTO public.sunumgorevlileri VALUES (529, 469, 100);
INSERT INTO public.sunumgorevlileri VALUES (530, 471, 198);
INSERT INTO public.sunumgorevlileri VALUES (531, 471, 199);
INSERT INTO public.sunumgorevlileri VALUES (532, 473, 77);
INSERT INTO public.sunumgorevlileri VALUES (533, 473, 78);
INSERT INTO public.sunumgorevlileri VALUES (534, 475, 197);
INSERT INTO public.sunumgorevlileri VALUES (535, 477, 107);
INSERT INTO public.sunumgorevlileri VALUES (536, 477, 108);
INSERT INTO public.sunumgorevlileri VALUES (537, 479, 130);
INSERT INTO public.sunumgorevlileri VALUES (538, 479, 129);
INSERT INTO public.sunumgorevlileri VALUES (539, 409, 129);
INSERT INTO public.sunumgorevlileri VALUES (540, 409, 130);
INSERT INTO public.sunumgorevlileri VALUES (541, 429, 161);
INSERT INTO public.sunumgorevlileri VALUES (542, 433, 173);
INSERT INTO public.sunumgorevlileri VALUES (543, 433, 160);


--
-- Name: adminbolumler_adminbolumid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.adminbolumler_adminbolumid_seq', 3, true);


--
-- Name: admins_adminid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admins_adminid_seq', 2, true);


--
-- Name: bolumler_bolumid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bolumler_bolumid_seq', 3, true);


--
-- Name: donemler_donemid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.donemler_donemid_seq', 1, true);


--
-- Name: duyurular_duyuruid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.duyurular_duyuruid_seq', 1, true);


--
-- Name: hocalar_hocaid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hocalar_hocaid_seq', 3, true);


--
-- Name: islemloglari_logid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.islemloglari_logid_seq', 1, false);


--
-- Name: konubasvurulari_basvuruid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.konubasvurulari_basvuruid_seq', 882, true);


--
-- Name: konular_konuid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.konular_konuid_seq', 60, true);


--
-- Name: mesajlar_mesajid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mesajlar_mesajid_seq', 1, false);


--
-- Name: ogrenciler_ogrenciid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ogrenciler_ogrenciid_seq', 220, true);


--
-- Name: sorubasvurulari_sorubasvuruid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sorubasvurulari_sorubasvuruid_seq', 1183, true);


--
-- Name: sorukontrolculeri_kontrolcuid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sorukontrolculeri_kontrolcuid_seq', 1, true);


--
-- Name: sunumgorevlileri_gorevid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sunumgorevlileri_gorevid_seq', 543, true);


--
-- Name: sunumprogrami_sunumid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sunumprogrami_sunumid_seq', 480, true);


--
-- PostgreSQL database dump complete
--

\unrestrict dWITauVBgTGRPH6AhRpw97kHs3DJPhCmm11DgUFFL9Tx6a8k5Kl1E35OXFL23sZ

