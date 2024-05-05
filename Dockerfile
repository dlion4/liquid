FROM python:3.12.3


ENV PYTHONUNBUFFERED=1


ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
