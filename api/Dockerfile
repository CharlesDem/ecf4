FROM python:3.11-slim

WORKDIR /app

COPY api/requirements-api.txt /tmp/requirements-api.txt
RUN pip install --no-cache-dir -r /tmp/requirements-api.txt

COPY api /app/api
COPY models /app/models

WORKDIR /app/api

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
