FROM python:3.12-alpine


ENV PYTHONUNBUFFERED=1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY . /app

# Set the working directory in the container
RUN pip install --upgrade pip setuptools wheel pyarrow


RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

RUN python manage.py compress --force

RUN python manage.py makemigrations
RUN python manage.py migrate




