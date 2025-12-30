# 1. Base Image: Use a lightweight Python 3.12 version (Linux based)
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies required for compiling llama-cpp-python
# 'build-essential' contains gcc/g++ compilers needed for C++ libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy necessary files from your PC to the Container
# We specifically copy the requirements first to leverage Docker cache
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code (including the GGUF model)
COPY . .

# 7. Expose the port Streamlit runs on
EXPOSE 8501

# 8. Command to run the app
# --server.address=0.0.0.0 is crucial for Docker networking
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]