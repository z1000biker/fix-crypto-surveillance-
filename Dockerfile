# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r surveillance-engine/requirements.txt

# Expose gRPC port
EXPOSE 50051

# Run the surveillance engine
CMD ["python", "surveillance-engine/main.py"]
