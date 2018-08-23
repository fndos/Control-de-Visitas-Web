
CREATE DATABASE educate;
USE educate;

INSERT INTO sector (id, name, is_active, created_by, date_joined) VALUES 
(1, 'Bolivar (Sagrario)', True, 'Alex Jordán', DATE_FORMAT(NOW(),'%Y-%m-%d')),  
(2, 'Acuarela', True, 'Alex Jordán', DATE_FORMAT(NOW(),'%Y-%m-%d')),
(3, 'Puerto Azul', True, 'Alex Jordán', DATE_FORMAT(NOW(),'%Y-%m-%d')),
(4, 'Las Orquídeas', True, 'Alex Jordán', DATE_FORMAT(NOW(),'%Y-%m-%d')),
(5, 'Batallón del Suburbio', True, 'Alex Jordán', DATE_FORMAT(NOW(),'%Y-%m-%d'));

INSERT INTO school VALUES 
(1,'09H02486','Unidad Educativa Domingo Savio','+593969488119','Tulcan 4502 Rosendo Áviles','Junto a la iglesia Domingo Savio',1,'Ayacucho',1,'Rafael Guerrero',1,'Alex Jordán',NULL,DATE_FORMAT(NOW(),'%Y-%m-%d'),NULL,1),
(2,'09H02570','Unidad Educativa Americo Vespucio','+593969488119','Calle Zamora 8 Ciudadela COVIEM','A dos cuadras del parque acuático COVIEM',1,'Ayacucho',1,'Rafael Guerrero',1,'Alex Jordán',NULL,DATE_FORMAT(NOW(),'%Y-%m-%d'),NULL,2);

INSERT INTO user (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, dni, phone_number, user_type, created_by, date_joined) VALUES 
(1, 'pbkdf2_sha256$100000$mEeRStxzv1wk$TG+/2P94ebK0JpUw6Lp/DlE/aNpWWiDX93vrSo4KmJw=', 1, 'tutor', 'Fernando', 'Sánchez', 'tutor@example.com', 1, 1, '2018-08-06 19:17:01.167838', '0929858736', '+593958477889', 1, 'Fernando Sánchez', DATE_FORMAT(NOW(),'%Y-%m-%d')),
(2, 'pbkdf2_sha256$100000$mEeRStxzv1wk$TG+/2P94ebK0JpUw6Lp/DlE/aNpWWiDX93vrSo4KmJw=', 1, 'tech', 'Jorge', 'Ayala', 'tech@example.com', 1, 1, '2018-08-06 19:17:01.167838', '1201333389', '+593958477889', 2, 'Fernando Sánchez', DATE_FORMAT(NOW(),'%Y-%m-%d')),
(3, 'pbkdf2_sha256$100000$mEeRStxzv1wk$TG+/2P94ebK0JpUw6Lp/DlE/aNpWWiDX93vrSo4KmJw=', 1, 'tutor_leader', 'Israel', 'Zurita', 'tutor_leader@example.com', 1, 1, '2018-08-06 19:17:01.167838', '1314344988', '+593958477889', 3, 'Fernando Sánchez', DATE_FORMAT(NOW(),'%Y-%m-%d')),
(4, 'pbkdf2_sha256$100000$mEeRStxzv1wk$TG+/2P94ebK0JpUw6Lp/DlE/aNpWWiDX93vrSo4KmJw=', 1, 'tech_leader', 'Alex', 'Jordán', 'tech_leader@example.com', 1, 1, '2018-08-06 19:17:01.167838', '3232848891', '+593958477889', 4, 'Fernando Sánchez', DATE_FORMAT(NOW(),'%Y-%m-%d'));

INSERT INTO requirement VALUES 
(1,'Mantenimiento de A/C',1,1,'Alex Jordán',NULL,DATE_FORMAT(NOW(),'%Y-%m-%d'),NULL,1,4,NULL),
(2,'Instalación de Software Antivirus',1,1,'Alex Jordán',NULL,DATE_FORMAT(NOW(),'%Y-%m-%d'),NULL,1,4,NULL),
(3,'Reparación de iluminación',1,1,'Alex Jordán',NULL,DATE_FORMAT(NOW(),'%Y-%m-%d'),NULL,2,4,NULL),
(4,'Visita Técnica Oficial',1,1,'Alex Jordán',NULL,DATE_FORMAT(NOW(),'%Y-%m-%d'),NULL,2,4,NULL);
