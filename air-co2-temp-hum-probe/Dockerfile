FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends i2c-tools \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir sensirion-i2c-driver sensirion-i2c-scd requests
COPY air-co2-temp-hum-probe.py /app/air-co2-temp-hum-probe.py
WORKDIR /app
CMD ["python", "air-co2-temp-hum-probe.py"]