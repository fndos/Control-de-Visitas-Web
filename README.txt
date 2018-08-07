- Clonar el repositorio
	git clone https://github.com/fndos/Control-de-Visitas-Web.git

- Instalar todas las herramientas y requerimientos necesarios
	Python 3.7 
	MySQL 5.7.22.1 	
	
	Descargar desde este enlace https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
	El archivo mysqlclient-1.3.13-cp37-cp37m-win32.whl

	pip install mysqlclient-1.3.13-cp37-cp37m-win32.whl

	pip install -r requirements.txt
	pip install django-phonenumber-field

- Crear una base de datos local
	CREATE DATABASE educate;
	NOTA: Cambiar la clave de la BD del archivo settings.py en el proyecto de Django

- Limpiar la caché del proyecto y migraciones. 
	Eliminar las 2 carpetas     __pycache__
	Eliminar la carpeta         migrations

- Realizar las migraciones del proyecto educate
	python manage.py makemigrations
	python manage.py migrate

- Realizar las migraciones de la aplicación accounts
	python manage.py makemigrations accounts
	python manage.py migrate accounts

- Crear 4 usuarios utilizando el script de INSERTS, que se encuentra alojado en la raíz del repositorio
	SQL File Educate.sql
	
- Finalmente ejecutar el servidor
	python manage.py runserver