FROM python:3.12-slim

RUN pip install requests

COPY api-data-probe.py /app/api-data-probe.py

CMD ["python", "/app/api-data-probe.py"]