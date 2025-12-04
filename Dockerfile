FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update && apt install -y \
    gcc \
    libpq-dev \
    libmagic1 \
    libmagic-dev \
    file \
    && apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Create static directory and collect static files
RUN mkdir -p /app/static
RUN python manage.py collectstatic --noinput || true

EXPOSE 5000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:5000"]