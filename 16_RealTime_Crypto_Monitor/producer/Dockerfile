# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY producer.py .

# Run the producer directly using python (unbuffered to see logs immediately)
CMD ["python", "-u", "producer.py"]