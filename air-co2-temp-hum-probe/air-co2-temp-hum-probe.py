import os
import requests
import time
import re

from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection
from sensirion_i2c_scd import Scd4xI2cDevice

API_BASE = os.environ.get("API_BASE", "http://localhost:8000")


def extract_numerical_value(obj):
    match = re.search(r"\d+(\.\d+)?", str(obj))
    return float(match.group()) if match else None


with LinuxI2cTransceiver("/dev/i2c-1") as i2c_transceiver:
    scd4x = Scd4xI2cDevice(I2cConnection(i2c_transceiver))
    time.sleep(1)

    scd4x.stop_periodic_measurement()
    print("scd4x Serial Number: {}".format(scd4x.read_serial_number()))

    scd4x.start_periodic_measurement()

    while True:
        time.sleep(10)
        co2, temperature, humidity = scd4x.read_measurement()
        co2_ppm = extract_numerical_value(co2)
        temperature_c = extract_numerical_value(temperature)
        humidity_rh = extract_numerical_value(humidity)
        print(
            "CO2: {} ppm, Temperature: {:.2f} °C, Humidity: {:.2f} %RH".format(
                co2_ppm, temperature_c, humidity_rh
            )
        )

        try:
            requests.post(
                f"{API_BASE}/ingest/scd4x",
                json={
                    "co2_ppm": co2_ppm,
                    "temperature_c": temperature_c,
                    "humidity_rh": humidity_rh,
                },
                timeout=2,
            )
        except Exception as e:
            print("Failed to send data to API:", e)
