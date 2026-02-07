# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Add src to Python path so imports work correctly
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Expose the port FastAPI will run on
EXPOSE 8000

# Default command to run the API
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]