"""
Read data from the Grove MGS V2 sensor and post it as JSON to the FastAPI backend.
Adapted from https://github.com/atsclct/atsc_sensors/blob/main/test_gas_gmxx_pi.py
"""
import time
import requests
from air_co_voc_no2_c2h5oh_probe import GAS_GMXXX

I2C_BUS = 0x01  # default use I2C1
import os
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")
API_URL = f"{API_BASE}/ingest/groove_mgs_v2"

gas = GAS_GMXXX(I2C_BUS, 0x08)


def post_data(g_no2: float, g_c2h5oh: float, g_voc: float, g_co: float) -> None:
    payload = {
        "NO2": g_no2,
        "C2H5OH": g_c2h5oh,
        "VOC": g_voc,
        "CO": g_co,
    }
    try:
        requests.post(API_URL, json=payload, timeout=2)
    except Exception as e:
        print("Failed to send data to API:", e)


def main() -> None:
    gas.preheat()
    for i in range(2):
        print(f"heating up {i}")
        time.sleep(1)

    while True:
        g_no2 = gas.calc_vol(gas.get_gm102b())
        g_c2h5oh = gas.calc_vol(gas.get_gm302b())
        g_voc = gas.calc_vol(gas.get_gm502b())
        g_co = gas.calc_vol(gas.get_gm702b())

        post_data(g_no2, g_c2h5oh, g_voc, g_co)
        time.sleep(10)


if __name__ == "__main__":
    main()
