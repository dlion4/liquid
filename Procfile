release: python manage.py migrate
web: gunicorn config.wsgi:application
heroku buildpacks:set heroku/python