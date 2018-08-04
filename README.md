## Control de Visitas (Web)

Primero, clonar el repositorio:

```bash
git clone https://github.com/fndos/Control-de-Visitas-Web.git
```

Prerrequesitos:

```bash
pip3 install django-phonenumber-field
```

Crear base de datos "educate" con mysql



Instalar los requerimientos

```bash
pip3 install -r requirements.txt
```

Crear la base de datos

```bash
python3 manage.py makemigrations

python3 manage.py migrate --run-syncdb

```

Finalmente, correr el servidor

```bash
python3 manage.py runserver
```

El proyecto estara en: **127.0.0.1:8000**
