# Official Python runtime
FROM python:3.9-slim

# Project work directorty
WORKDIR /eventcalendar

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the local project directory to the container
COPY requirements.txt /eventcalendar/

# Install module dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /eventcalendar

# Expose the port for public access
EXPOSE 8001

# Command to run the Django application (using Gunicorn for production)
CMD ["gunicorn", "eventcalendar.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "2"]

