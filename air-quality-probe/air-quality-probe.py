import serial
import time
from influxdb import InfluxDBClient
from tenacity import retry, stop_after_attempt, wait_fixed
from datetime import datetime

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def write_data_to_influxdb(pm25, pm10):
    """
    Tries to write the data to the database, and if it fails, waits 2 seconds and tries again. 
    It will do this 5 times, and if it still fails, it will give up.
    :param pm25: PM2.5 concentration in µg/m3
    :param pm10: PM10 concentration in µg/m³
    """
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

# Initialize serial connection outside the loop
ser = serial.Serial('/dev/ttyUSB0')

while True:
    client = InfluxDBClient(host='influxdb', port=8086)
    client.create_database('sds011_data')
    client.switch_database('sds011_data')

    data = []
    
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)
    
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    
    print(f"{datetime.now()}: PM 2.5: {pmtwofive} µg/m³, PM 10: {pmten} µg/m³")
    
    if pmtwofive is not None and pmten is not None:
        write_data_to_influxdb(pmtwofive, pmten)
    
    print(f"{datetime.now()}: Sleeping for 10 seconds")
    time.sleep(10)
    print(f"{datetime.now()}: Woke up from sleep")
    
    client.close()
