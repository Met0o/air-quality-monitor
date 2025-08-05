FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip i2c-tools && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir bme680 requests numpy
COPY air-voc-probe.py iaq.py /app/
WORKDIR /app
CMD ["python", "air-voc-probe.py"]