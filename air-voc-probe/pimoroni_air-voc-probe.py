import bme680
import time
import requests

import os
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")
API_URL = f"{API_BASE}/ingest/bme680"

def post_data(air_quality_score, gas, hum, pressure):
    payload = {
        "air_quality_score": air_quality_score,
        "gas_resistance": gas,
        "humidity": hum,
        "pressure": pressure,
    }
    try:
        requests.post(API_URL, json=payload, timeout=2)
    except Exception as e:
        print("Failed to send data to API:", e)


def main():
    try:
        sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except (RuntimeError, IOError):
        sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)

    start_time = time.time()
    burn_in_time = 300
    burn_in_data = []

    print("Collecting gas resistance burn-in data for 5 mins\n")
    while time.time() - start_time < burn_in_time:
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            burn_in_data.append(gas)
            print(f"Gas: {gas} Ohms")
            time.sleep(1)

    gas_baseline = sum(burn_in_data[-50:]) / 50.0
    hum_baseline = 40.0
    hum_weighting = 0.25

    print(f"Gas baseline: {gas_baseline} Ohms, humidity baseline: {hum_baseline:.2f} %RH\n")

    while True:
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            gas_offset = gas_baseline - gas

            hum = sensor.data.humidity
            hum_offset = hum - hum_baseline

            pressure = sensor.data.pressure

            if hum_offset > 0:
                hum_score = (100 - hum_baseline - hum_offset)
                hum_score /= (100 - hum_baseline)
                hum_score *= (hum_weighting * 100)
            else:
                hum_score = (hum_baseline + hum_offset)
                hum_score /= hum_baseline
                hum_score *= (hum_weighting * 100)

            if gas_offset > 0:
                gas_score = (gas / gas_baseline)
                gas_score *= (100 - (hum_weighting * 100))
            else:
                gas_score = 100 - (hum_weighting * 100)

            air_quality_score = hum_score + gas_score

            print(
                f"Gas: {gas:.2f} Ohms,humidity: {hum:.2f} %RH,air quality: {air_quality_score:.2f},pressure: {pressure:.2f} hPa"
            )

            post_data(air_quality_score, gas, hum, pressure)
            time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
