FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_tinyllama.py .
COPY templates/ templates/

EXPOSE 5000

CMD ["python", "app_tinyllama.py"]
