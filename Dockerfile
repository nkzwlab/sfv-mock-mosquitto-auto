FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY publisher.py .
COPY requests/ requests/

CMD ["python", "publisher.py"]
