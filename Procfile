release: python manage.py migrate

web: gunicorn config.wsgi

heroku buildpacks:set heroku/python