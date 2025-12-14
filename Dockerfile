# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY app/requirements.txt .

# Install Python dependencies and curl for healthchecks
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY app/ .

# Expose port 5001
EXPOSE 5001

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "main:app"]

