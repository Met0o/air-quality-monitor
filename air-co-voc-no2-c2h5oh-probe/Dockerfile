FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends i2c-tools \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir smbus2 requests
COPY air_co_voc_no2_c2h5oh_probe.py air-co-voc-no2-c2h5oh-call.py /app/
WORKDIR /app
CMD ["python", "air-co-voc-no2-c2h5oh-call.py"]