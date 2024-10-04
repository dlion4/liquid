FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /api

COPY . /api

# Copy the entrypoint scripts and make them executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# Expose port 8000 for the Django app

EXPOSE 8001

CMD [ "/bin/bash", "/api/entrypoint.sh" ]
