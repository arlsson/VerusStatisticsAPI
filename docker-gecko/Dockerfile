FROM python:3.11-slim

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir -r docker-gecko/requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--log-level", "debug", "--proxy-headers" ]
