FROM python:3.9

RUN pip install influxdb pyserial tenacity

COPY air-quality-probe.py /app/air-quality-probe.py

CMD ["python", "/app/air-quality-probe.py"]