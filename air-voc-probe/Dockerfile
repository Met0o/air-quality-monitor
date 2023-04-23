FROM python:3.9

RUN pip install --upgrade pip numpy influxdb pyserial bme680

COPY air-voc-probe.py /app/air-voc-probe.py
COPY iaq.py /app/iaq.py

CMD ["python", "/app/air-voc-probe.py"]