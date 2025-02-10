# api/Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables for Flask development with hot reloading
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Expose the API port
EXPOSE 5000

# Run Flask with hot reloading enabled
CMD ["flask", "run", "--reload", "--host=0.0.0.0"]