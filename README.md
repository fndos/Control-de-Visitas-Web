## Control de Visitas (Web)

Primero, clonar el repositorio:

```bash
git clone https://github.com/fndos/Control-de-Visitas-Web.git
```

Instalar los requerimientos

```bash
pip install -r requirements.txt
```

Crear la base de datos

```bash
python manage.py makemigrations

python manage.py migrate --run-syncdb

```

Finalmente, correr el servidor

```bash
python manage.py runserver
```

El proyecto estara en: **127.0.0.1:8000**
