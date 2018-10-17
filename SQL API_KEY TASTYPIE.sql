--# CREAR USUARIO SYSTEM
INSERT INTO user (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, dni, phone_number, user_type, created_by, updated_by, date_joined, date_updated) VALUES
(5, 'pbkdf2_sha256$100000$mEeRStxzv1wk$TG+/2P94ebK0JpUw6Lp/DlE/aNpWWiDX93vrSo4KmJw=', 1, 'system', 'Admin', 'System', 'adminsystem@example.com', 1, 1, '0000000001', '+593000000009', 1, 'Admin System', 'Admin System', DATE_FORMAT(NOW(),'%Y-%m-%d'), DATE_FORMAT(NOW(),'%Y-%m-%d'));

--# CREAR API_KEY PARA EL TASTYPIE
INSERT INTO tastypie_apikey VALUES (DEFAULT,'ABC123456789',CURRENT_TIMESTAMP,5);
