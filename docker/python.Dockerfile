FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy Python requirements first (for caching)
COPY requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual Python API code
COPY app ./app

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
