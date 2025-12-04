FROM python:3.12-slim

# Prevent Python from writing .pyc files & buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (Postgres, libmagic, build tools)
RUN apt update && apt install -y \
    gcc \
    libpq-dev \
    libmagic1 \
    libmagic-dev \
    file \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose Django port
EXPOSE 5000

# Run migrations and start Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:5000"]
