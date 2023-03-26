FROM python:3.9

RUN pip install influxdb requests

COPY api-data-probe.py /app/api-data-probe.py

CMD ["python", "/app/api-data-probe.py"]