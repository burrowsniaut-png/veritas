<<<<<<< HEAD
FROM python:3.11-slim

# Install Ollama
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python deps
RUN pip install -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 5000

# Start Ollama, pull model, then start app
CMD ollama serve & \
    sleep 5 && \
    ollama pull llama3.2:1b && \
    python veritas_web_app.py
=======
# Use a Python base image
FROM python:3.11-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    librandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .

CMD ["python", "veritas_web_app.py"]
>>>>>>> abdb0e55ebc00c95eb3a1e964f7ac92e5ba94369
