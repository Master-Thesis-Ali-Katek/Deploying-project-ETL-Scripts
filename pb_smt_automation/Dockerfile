# Use the latest Python image
FROM python:3.13

# Set the working directory inside the container
WORKDIR /main

# Copy only necessary files first (to leverage Docker caching)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables (if needed)
ENV PYTHONUNBUFFERED=1

# Define the command to run your Python script
CMD ["python", "main.py"]
