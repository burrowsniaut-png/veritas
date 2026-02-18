FROM python:3.11-slim

# Install Ollama and unzip
RUN apt-get update && apt-get install -y curl unzip && \
    curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python deps
RUN pip install -r requirements.txt

# Copy app files
COPY . .

# Extract templates.zip if it exists
RUN if [ -f templates.zip ]; then unzip templates.zip && rm templates.zip; fi

# Expose port
EXPOSE 5000

# Start Ollama, pull model, then start app
CMD ollama serve & \
    sleep 5 && \
    ollama pull llama3.2:1b && \
    python veritas_web_app.py
