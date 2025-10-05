FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY docker/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    python -c "import flask; print('Flask installed successfully')"

# Copy application code
COPY scripts/webhook-receiver.py webhook-receiver.py

# Expose port
EXPOSE 9000

# Run the application
CMD ["python", "webhook-receiver.py"]
