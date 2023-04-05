FROM python:3.9

COPY driver /app/driver

RUN cd /app/driver && \
    make

RUN apt-get update && \
    apt-get install -y i2c-tools wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install influxdb pyserial tenacity smbus2 sensirion-i2c-sen5x sensirion-i2c-scd

COPY air-co2-temp-hum-probe.py /app/air-co2-temp-hum-probe.py

CMD ["python", "/app/air-co2-temp-hum-probe.py"]
