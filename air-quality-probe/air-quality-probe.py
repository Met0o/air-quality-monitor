import os
import time
import serial
import requests
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed


API_BASE = os.environ.get("API_BASE", "http://localhost:8000")
API_URL = f"{API_BASE}/ingest/sds011"

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def post_data(pm25: float, pm10: float) -> None:
    """
    Post particulate matter readings to the FastAPI service.
    Retries automatically on temporary network failures.
    """
    payload = {"PM25": pm25, "PM10": pm10}
    requests.post(API_URL, json=payload, timeout=2)


def main() -> None:
    ser = serial.Serial('/dev/ttyUSB0')

    while True:
        data = [ser.read() for _ in range(10)]
        pm25 = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
        pm10 = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

        print(f"{datetime.now()}: PM 2.5: {pm25} µg/m³, PM 10: {pm10} µg/m³")

        if pm25 is not None and pm10 is not None:
            try:
                post_data(pm25, pm10)
            except Exception as e:
                print("Failed to post data:", e)

        print(f"{datetime.now()}: Sleeping for 10 seconds")
        time.sleep(10)


if __name__ == "__main__":
    main()
