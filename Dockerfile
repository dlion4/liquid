FROM python:3.12


ENV PYTHONUNBUFFERED=1


ENV PYTHONDONTWRITEBYTECODE=1

ENV PORT=8000

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

EXPOSE $PORT


ENTRYPOINT ["/app/compose/entrypoint"]