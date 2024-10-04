# Use the official Python image from the Docker Hub
FROM python:3.10-slim-buster


ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install virtualenv
RUN pip install virtualenv

# remove the xisting virtual env 
# RUN rm -rf /app/.venv
# Create virtual environment
RUN virtualenv /app/.venv

# Activate virtual environment and install dependencies
RUN /bin/bash -c "source /app/.venv/bin/activate && pip install --upgrade pip && pip install --default-timeout=1000 --retries 10 -r requirements.txt"

# Copy the entrypoint scripts and make them executable
COPY entrypoint.sh /app/entrypoint.sh
COPY collectstatic.sh /app/collectstatic.sh
COPY build_files.sh /app/build_files.sh

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/collectstatic.sh
RUN chmod +x /app/build_files.sh

# Expose port 8000 for the Django app
EXPOSE 8000
EXPOSE 8090
EXPOSE 8091
EXPOSE 8078


# Run entrypoint.sh
CMD ["/bin/bash", "/app/entrypoint.sh"]

