# Use a lightweight Python image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /main

# Copy all necessary files
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container starts
CMD ["python", "main.py"]
