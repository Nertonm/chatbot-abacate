# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Create a non-root user for safety
RUN useradd --create-home appuser || true

WORKDIR /app

# Copy requirements and install in one layer; no cache to keep image smaller
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy only what we need (use .dockerignore to keep context small)
COPY . /app

# Make scripts executable
RUN chmod +x /app/scripts/wait-for-db.sh /app/scripts/docker-entrypoint.sh || true

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Copy DB init scripts if provided (kept for compatibility)
RUN [ -f init_db.sql ] && cp init_db.sql /docker-entrypoint-initdb.d/ || true
RUN [ -f init_db.sh ] && cp init_db.sh /docker-entrypoint-initdb.d/ || true

USER appuser

ENTRYPOINT ["bash", "/app/scripts/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]