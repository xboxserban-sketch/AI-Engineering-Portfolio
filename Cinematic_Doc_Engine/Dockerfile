# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables for production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

# Set work directory
WORKDIR $APP_HOME

# Install system dependencies (e.g., ffmpeg for media processing)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
# Fallback in case requirements.txt is empty or missing in the prototype
RUN touch requirements.txt 
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project
COPY . .

# Create a non-root user for security (Best Practice / Senior level)
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser $APP_HOME
USER appuser

# Default command
CMD ["python", "generate_doc.py"]
