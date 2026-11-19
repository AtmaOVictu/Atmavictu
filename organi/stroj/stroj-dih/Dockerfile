FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
RUN pip install --no-cache-dir "mistralai-workflows>=3.10"
COPY src ./src
CMD ["python", "-u", "-m", "worker.entrypoints.worker"]
