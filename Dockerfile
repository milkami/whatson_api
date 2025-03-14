FROM python:3.12.8-alpine3.21

# Environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libpq \
    postgresql-dev \
    python3-dev \
    py3-pip \
    build-base

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app

# Expose port 8001
EXPOSE 8001

# Collect static files
RUN python manage.py collectstatic --noinput

# Start application
CMD ["sh", "run"]

