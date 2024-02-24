import time
import re

from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection
from sensirion_i2c_scd import Scd4xI2cDevice
from influxdb import InfluxDBClient

def write_data_to_influxdb(co2, temperature, humidity):
    """
    The function `write_data_to_influxdb` writes CO2, temperature, and humidity data to an InfluxDB
    database.
    
        :param co2: Carbon Dioxide (CO2) concentration in parts per million (ppm)
        :param temperature: The `write_data_to_influxdb` function you provided is used to write CO2,
        temperature, and humidity data to an InfluxDB database
        :param humidity: Humidity is the amount of water vapor present in the air. It is typically expressed
        as a percentage and represents the relative humidity in the environment
    """
    data = [
        {
            "measurement": "scd4x",
            "fields": {
                "CO2": co2,
                "Temperature": temperature,
                "Humidity": humidity,
            }
        }
    ]

    client.write_points(data)

def extract_numerical_value(obj):
    match = re.search(r'\d+(\.\d+)?', str(obj))
    return float(match.group()) if match else None

with LinuxI2cTransceiver('/dev/i2c-1') as i2c_transceiver:

    scd4x = Scd4xI2cDevice(I2cConnection(i2c_transceiver))
    time.sleep(1)

    scd4x.stop_periodic_measurement()
    print("scd4x Serial Number: {}".format(scd4x.read_serial_number()))

    scd4x.start_periodic_measurement()

    client = InfluxDBClient(host='influxdb', port=8086)
    client.create_database('scd4x_data')
    client.switch_database('scd4x_data')

    while True:
        time.sleep(5)
        co2, temperature, humidity = scd4x.read_measurement()
        co2_ppm = extract_numerical_value(co2)
        temperature_c = extract_numerical_value(temperature)
        humidity_rh = extract_numerical_value(humidity)
        print("CO2: {} ppm, Temperature: {:.2f} °C, Humidity: {:.2f} %RH".format(co2_ppm, temperature_c, humidity_rh))
        
        write_data_to_influxdb(co2_ppm, temperature_c, humidity_rh)