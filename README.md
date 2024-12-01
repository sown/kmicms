# SUWS / SOWN Wagtail CMS

## Development

The website is currently intended to be developed outside of docker, using a SQLite database.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp kmicms/kmicms/configuration.dev.py kmicms/kmicms/configuration.py

cd kmicms
./manage.py migrate
./manage.py runserver
```

To create an initial user: `./manage.py createsuperuser`

## Production

The website is intended to be deployed using the Docker Compose configuration.

You need to create a `.env` file containing the secrets:

```
SECRET_KEY=django-insecure-rT1fjisdfhsdfsiof3fsdfjs9d0fwqe78(UO-X^FPe

SSO_OIDC_CONFIGURATION_URL=https://sso.example.com/.well-known/openid-configuration
SSO_OIDC_CLIENT_ID=YourClientIdHere
SSO_OIDC_CLIENT_SECRET=YourClientSecretHere
SSO_STAFF_GROUP_NAME=kmicms:staff
SSO_SUPERUSER_GROUP_NAME=kmicms:superuser

NETBOX_API_TOKEN=abc
```

There is an example of this file: `.env.example`

```
docker compose up
```