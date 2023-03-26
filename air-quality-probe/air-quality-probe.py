import serial
import time

from influxdb import InfluxDBClient
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def write_data_to_influxdb(pm25, pm10):
    
    data = [
        {
            "measurement": "sds011",
            "fields": {
                "PM25": pm25,
                "PM10": pm10,
            }
        }
    ]
    
    client.write_points(data)

ser = serial.Serial('/dev/ttyUSB0')

client = InfluxDBClient(host='influxdb', port=8086)
client.create_database('sds011_data')
client.switch_database('sds011_data')

while True:
    
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)
    
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    
    print(f"PM 2.5: {pmtwofive} µg/m³, PM 10: {pmten} µg/m³")
    
    if pmtwofive is not None and pmten is not None:
        write_data_to_influxdb(pmtwofive, pmten)
    
    time.sleep(10)

client.close()