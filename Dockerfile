# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Install FFmpeg and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir git+https://github.com/openai/whisper.git

# Set up working directory
WORKDIR /app

# Add a script to handle transcription
COPY transcribe.py /app/transcribe.py

# Add a script to fetch model data at build time
COPY load.py /app/load.py

RUN python /app/load.py

# Set entrypoint to handle file input/output
ENTRYPOINT ["python", "/app/transcribe.py"]
