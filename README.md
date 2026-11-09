# Oulu Weather Dashboard

A responsive Django weather dashboard for Oulu, Finland. Uses [Open-Meteo](https://open-meteo.com/) without an API key for non-commercial use.

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Activate: macOS/Linux: source .venv/bin/activate; Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Production hosting

GitHub Pages cannot run Django. On Render or another Python host, set build command `pip install -r requirements.txt && python manage.py collectstatic --noinput` and start command `gunicorn oulu_weather.wsgi:application`. Configure `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, and `DJANGO_ALLOWED_HOSTS` for your host. No database is required.

Weather data supplied by Open-Meteo; actual update frequency depends on the provider.
