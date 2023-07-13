FROM python:3.9

RUN pip install --upgrade pip influxdb smbus

COPY air_co_voc_no2_c2h5oh_probe.py /app/air_co_voc_no2_c2h5oh_probe.py
COPY air-co-voc-no2-c2h5oh-call.py /app/air-co-voc-no2-c2h5oh-call.py

CMD ["python", "/app/air-co-voc-no2-c2h5oh-call.py"]