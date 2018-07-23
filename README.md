## Ejecutar el proyecto localmente

Primero, clonar el repositorio:

```bash
git clone https://github.com/sibtc/django-multiple-user-types-example.git
```

Instalar los requerimientos

```bash
pip3 install -r requirements.txt
```

Crear la base de datos

```bash
python3 manage.py makemigrations

python3 manage.py migrate --run-syncdb

```

Finalmente, corre el servidor

```bash
python3 manage.py runserver
```

El proyecto estara en: **127.0.0.1:8000**.


## License

Propietario???
