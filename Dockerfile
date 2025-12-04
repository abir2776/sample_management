FROM python:3.12-slim

# Prevent Python from writing .pyc files & buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install required system packages
RUN apt update && apt install -y gcc libpq-dev

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Run Django migrations & start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:5000"]
