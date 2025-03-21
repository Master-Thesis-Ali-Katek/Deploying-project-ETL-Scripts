# Use the lightweight Python image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /main

# Copy all files into the container
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the main script when the container starts
CMD ["python", "main.py"]
