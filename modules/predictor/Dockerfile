FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required by numpy, pyaudio, etc.
RUN apt-get update && \
    apt-get install -y \
        gcc \
        g++ \
        libatlas-base-dev \
        portaudio19-dev \
        libffi-dev \
        libssl-dev \
        python3-dev \
        curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY predictor.py .
COPY model.eim .
RUN chmod +x model.eim

CMD ["python", "predictor.py"]
