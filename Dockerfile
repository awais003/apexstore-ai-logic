# Development Dockerfile for fast iteration with hot-reload
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# 1. Copy ONLY the requirements first
COPY requirements.txt .

# 2. Install dependencies (This layer is CACHED unless requirements.txt changes)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of the application code
COPY . .

# Run the service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]