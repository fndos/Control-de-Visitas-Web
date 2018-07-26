- Clonar el repositorio
	git clone https://github.com/fndos/Control-de-Visitas-Web.git

- Instalar todas las herramientas y requerimientos necesarios
	Python 3.7 
	MySQL 5.7.22.1 	
	
	Descargar desde este enlace https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
	El archivo mysqlclient-1.3.13-cp37-cp37m-win32.whl

	pip install mysqlclient-1.3.13-cp37-cp37m-win32.whl

	pip install -r requirements.txt

- Crear una base de datos local
	CREATE DATABASE educate
	NOTA: Cambiar la clave de la BD del archivo settings.py en el proyecto de Django

- Realizar las migraciones  
	python manage.py makemigrations
	python manage.py migrate --run-syncdb

- Crear 4 super usuarios utilizando el siguiente comando
	python manage.py createsuperuser
	
	Se recomienda considerar el siguiente orden
	
		Username: tutor
		Email:    tutor@example.com
		Password: feducate

		Username: tutor_leader
		Email:    tutor_leader@example.com
		Password: feducate

		Username: tech
		Email:    tech@example.com
		Password: feducate

		Username: tech_leader
		Email:    tech_leader@example.com
		Password: feducate

- Ejecutar los siguientes comandos en MySQL
	USE educate
	SELECT* FROM accounts_user

	UPDATE accounts_user 
SET first_name='Fernando', last_name='Sánchez', is_tutor=1 
WHERE id=1; 


	UPDATE accounts_user 
SET first_name='Jorge', last_name='Ayala', is_tutor=1, is_leader=1 
WHERE id=2; 


	UPDATE accounts_user
 SET first_name='Israel', last_name='Zurita', is_tech=1 
WHERE id=3; 


	UPDATE accounts_user
 SET first_name='Alex', last_name='Jordán', is_tech=1, is_leader=1 
WHERE id=4; 

	SELECT* FROM accounts_user

- Finalmente ejecutar el servidor
	python manage.py runserver