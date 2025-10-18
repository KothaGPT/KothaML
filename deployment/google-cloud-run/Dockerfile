# Multi-stage build for efficiency
FROM python:3.9-slim-buster as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim-buster
RUN groupadd -r app && useradd -r -g app app
RUN groupadd -r app && useradd -r -g app app
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN chown -R app:app /app
USER app
CMD ["gunicorn", "-w", "4", "--worker-class", "gthread", "-b", "0.0.0.0:8080", "docker-entrypoint:app"]
EXPOSE 8080