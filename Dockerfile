# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY examples ./examples
COPY tests ./tests
COPY README.md .
COPY main.py .

ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
