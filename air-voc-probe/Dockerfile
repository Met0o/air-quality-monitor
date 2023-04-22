FROM python:3.9

RUN pip install influxdb pyserial bme680

COPY air-voc-probe.py /app/air-voc-probe.py

CMD ["python", "/app/air-voc-probe.py"]