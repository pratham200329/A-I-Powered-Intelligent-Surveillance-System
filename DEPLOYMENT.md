# Deployment Guide

## Local deployment

1. Install Python 3.10 or 3.11
2. Create virtual environment and install dependencies:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

3. Configure environment:

copy .env.example .env

4. Start service:

python run_backend.py

5. Open dashboard:

http://localhost:8000

## Docker deployment

1. Build and run:

docker compose up --build

2. Service URL:

http://localhost:8000

## GPU deployment recommendation

- Use an NVIDIA-enabled base image
- Install CUDA-compatible PyTorch and ultralytics stack
- Use larger YOLO models (yolov8m or yolov8l) if latency allows
- Pin inference workers to dedicated GPUs

## Cloud deployment pattern

- API layer: FastAPI container (autoscaled)
- Inference workers: dedicated CV workers consuming camera streams
- Storage: PostgreSQL + object store for video snippets
- Alerts: event bus + notification service
- Monitoring: Prometheus/Grafana + structured logs

## Security hardening checklist

- Enforce API authentication and RBAC
- Encrypt data at rest and in transit
- Rotate SMTP/Twilio credentials
- Enable audit trails for alert actions
- Retain only policy-approved biometric data duration
