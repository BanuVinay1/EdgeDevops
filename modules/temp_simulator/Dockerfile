FROM python:3.9-slim

WORKDIR /app

COPY temp_simulator.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "temp_simulator.py"]
