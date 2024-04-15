import numpy as np
import bme680

from influxdb import InfluxDBClient
from time import *
from iaq import *

client = InfluxDBClient(host='influxdb', port=8086)
client.create_database('bme680_data')
client.switch_database('bme680_data')

def write_data_to_influxdb(air_quality_score, gas, hum, pressure, temp):
    if air_quality_score is None:
        print("Air quality score is None, skipping data point.")
        return

    data = [
        {
            "measurement": "bme680",
            "fields": {
                "air_quality_score": float(air_quality_score),
                "gas_resistance": float(gas),
                "humidity": float(hum),
                "pressure": float(pressure),
                "temp": float(temp)
            }
        }
    ]
    
    client.write_points(data)

bme680_temp_offset = 0 #-4.5 #temperature offset: depends on heating profile and external heat sources close to mounting point (i.e. Raspberry Pi SoC)
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
sensor680.get_sensor_data()

temp = 0
press = 0
hum = 0
R_gas = 0

def prompt_data(temp, press, hum, Rgas, AQ):	
	out_string = "{0}: {1:.2f}°C, {2:.2f}hPa, {3:.2f}%RH, {4:.1f}kOhm".format(strftime("%Y-%m-%d %H:%M:%S"),temp,press,hum,Rgas/1000)
	if AQ == None:
		out_string += ", cal."
	else:
		out_string += ", {0:.1f}%aq".format(AQ)
	print(out_string)
	
iaq_tracker = IAQTracker()

while True:
	if sensor680.get_sensor_data():
		temp = sensor680.data.temperature
		press = sensor680.data.pressure
		hum = sensor680.data.humidity
		
		if sensor680.data.heat_stable:
			R_gas = sensor680.data.gas_resistance
			AQ = iaq_tracker.getIAQ(sensor680.data)
		else:
			R_gas = 0
			AQ = None
			
		prompt_data(temp, press, hum, R_gas, AQ)

		write_data_to_influxdb(AQ, R_gas, hum, press, temp)
  
	sleep(1)