import bme680
import requests
from time import sleep, strftime
from iaq import IAQTracker

import os
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")
API_URL = f"{API_BASE}/ingest/bme680"

def post_data(air_quality_score, gas, hum, pressure, temp):
    payload = {
        "gas_resistance": float(gas),
        "humidity": float(hum),
        "pressure": float(pressure),
        "temp": float(temp),
    }
    
    # Only add air quality score if it's available (not during calibration)
    if air_quality_score is not None:
        payload["air_quality_score"] = float(air_quality_score)
        print("Sending data with air quality score:", air_quality_score)
    else:
        print("Sending data without air quality score (still calibrating)")
    
    try:
        requests.post(API_URL, json=payload, timeout=2)
    except Exception as e:
        print("Failed to send data to API:", e)


def prompt_data(temp, press, hum, rgas, aq):
    out = "{0}: {1:.2f}°C, {2:.2f}hPa, {3:.2f}%RH, {4:.1f}kOhm".format(
        strftime("%Y-%m-%d %H:%M:%S"),
        temp,
        press,
        hum,
        rgas / 1000,
    )
    if aq is None:
        out += ", cal."
    else:
        out += ", {0:.1f}%aq".format(aq)
    print(out)


def main():
    bme680_temp_offset = 0
    sensor680 = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

    sensor680.set_humidity_oversample(bme680.OS_2X)
    sensor680.set_pressure_oversample(bme680.OS_4X)
    sensor680.set_temperature_oversample(bme680.OS_8X)
    sensor680.set_filter(bme680.FILTER_SIZE_3)
    sensor680.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor680.set_gas_heater_temperature(320)
    sensor680.set_gas_heater_duration(150)
    sensor680.select_gas_heater_profile(0)
    sensor680.set_temp_offset(bme680_temp_offset)

    iaq_tracker = IAQTracker()

    while True:
        if sensor680.get_sensor_data():
            temp = sensor680.data.temperature
            press = sensor680.data.pressure
            hum = sensor680.data.humidity

            if sensor680.data.heat_stable:
                r_gas = sensor680.data.gas_resistance
                aq = iaq_tracker.getIAQ(sensor680.data)
            else:
                r_gas = 0
                aq = None

            prompt_data(temp, press, hum, r_gas, aq)
            post_data(aq, r_gas, hum, press, temp)
            sleep(10)


if __name__ == "__main__":
    main()
