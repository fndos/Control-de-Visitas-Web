
CREATE DATABASE educate;
USE educate;

INSERT INTO accounts_user (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, dni, phone_number, user_type) 
VALUES (1, 'pbkdf2_sha256$100000$mEeRStxzv1wk$TG+/2P94ebK0JpUw6Lp/DlE/aNpWWiDX93vrSo4KmJw=', 1, 'tutor', 'Fernando', 'Sánchez', 'tutor@example.com', 1, 1, '2018-08-06 19:17:01.167838', '0929858736', '+593958477889', 1);

INSERT INTO accounts_user (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, dni, phone_number, user_type) 
VALUES (2, 'pbkdf2_sha256$100000$mEeRStxzv1wk$TG+/2P94ebK0JpUw6Lp/DlE/aNpWWiDX93vrSo4KmJw=', 1, 'tech', 'Jorge', 'Ayala', 'tech@example.com', 1, 1, '2018-08-06 19:17:01.167838', '1201333389', '+593958477889', 2);

INSERT INTO accounts_user (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, dni, phone_number, user_type) 
VALUES (3, 'pbkdf2_sha256$100000$mEeRStxzv1wk$TG+/2P94ebK0JpUw6Lp/DlE/aNpWWiDX93vrSo4KmJw=', 1, 'tutor_leader', 'Israel', 'Zurita', 'tutor_leader@example.com', 1, 1, '2018-08-06 19:17:01.167838', '1314344988', '+593958477889', 3);

INSERT INTO accounts_user (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, dni, phone_number, user_type) 
VALUES (4, 'pbkdf2_sha256$100000$mEeRStxzv1wk$TG+/2P94ebK0JpUw6Lp/DlE/aNpWWiDX93vrSo4KmJw=', 1, 'tech_leader', 'Alex', 'Jordán', 'tech_leader@example.com', 1, 1, '2018-08-06 19:17:01.167838', '3232848891', '+593958477889', 4);