# SUWS Wagtail CMS

## Development

The website is currently intended to be developed outside of docker, using a SQLite database.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp sowncms/sowncms/configuration.dev.py sowncms/sowncms/configuration.py

cd sowncms
./manage.py migrate
./manage.py runserver
```

To create an initial user: `./manage.py createsuperuser`

## Production

The website is intended to be deployed using the Docker Compose configuration.

You need to create a `.env` file containing the secrets:

```
SECRET_KEY=django-insecure-rT1fjisdfhsdfsiof3fsdfjs9d0fwqe78(UO-X^FPe
```

There is an example of this file: `.env.example`

```
docker compose up
```