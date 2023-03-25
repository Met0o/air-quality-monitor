FROM python:3.9

RUN pip install influxdb pyserial
RUN pip install tenacity

COPY air_quality_probe.py /app/air_quality_probe.py

CMD ["python", "/app/air_quality_probe.py"]