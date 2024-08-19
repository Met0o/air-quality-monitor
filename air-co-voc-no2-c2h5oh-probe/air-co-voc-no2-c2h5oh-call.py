'''
# Adapted from https://github.com/atsclct/atsc_sensors/blob/main/test_gas_gmxx_pi.py
'''
import time, smbus
from influxdb import InfluxDBClient
from air_co_voc_no2_c2h5oh_probe import *

I2C_BUS = 0x01  # default use I2C1

# The default address for i2c gas_gmxx is 0x08
gas = GAS_GMXXX(I2C_BUS ,0x08)

gas.preheat()
for i in range(2):
    print('heating up ' + str(i))
    time.sleep(1)

client = InfluxDBClient(host='influxdb', port=8086)
client.create_database('groove_mgs_v2_data')
client.switch_database('groove_mgs_v2_data')

def write_data_to_influxdb(g_no2, g_c2h5oh, g_voc, g_co):
    data = [
        {
            "measurement": "groove_mgs_v2",
            "fields": {
                "NO2": float(g_no2),
                "C2H5OH": float(g_c2h5oh),
                "VOC": float(g_voc),
                "CO": float(g_co)
            }
        }
    ]
    client.write_points(data)

def loop():
    g_no2 = gas.calc_vol(gas.get_gm102b())
    g_c2h5oh = gas.calc_vol(gas.get_gm302b())
    g_voc = gas.calc_vol(gas.get_gm502b())
    g_co = gas.calc_vol(gas.get_gm702b())
    
    write_data_to_influxdb(g_no2, g_c2h5oh, g_voc, g_co)
    
    time.sleep(10)

if __name__ == "__main__":
    while True:
        loop()