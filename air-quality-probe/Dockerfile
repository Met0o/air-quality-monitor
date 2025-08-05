FROM python:3.12-slim

RUN pip install --no-cache-dir pyserial requests tenacity
COPY air-quality-probe.py /app/air-quality-probe.py
WORKDIR /app

CMD ["python", "air-quality-probe.py"]