import bme680
import time

from influxdb import InfluxDBClient

def write_data_to_influxdb(air_quality_score, gas, hum, pressure):
    data = [
        {
            "measurement": "bme680",
            "fields": {
                "air_quality_score": air_quality_score,
                "gas_resistance": gas,
                "humidity": hum,
                "pressure": pressure
            }
        }
    ]
    
    client.write_points(data)

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
curr_time = time.time()
burn_in_time = 300

burn_in_data = []

try:
    print('Collecting gas resistance burn-in data for 5 mins\n')
    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            burn_in_data.append(gas)
            print('Gas: {0} Ohms'.format(gas))
            time.sleep(1)

    gas_baseline = sum(burn_in_data[-50:]) / 50.0
    hum_baseline = 40.0
    hum_weighting = 0.25

    print('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(
        gas_baseline,
        hum_baseline))

    client = InfluxDBClient(host='influxdb', port=8086)
    client.create_database('bme680_data')
    client.switch_database('bme680_data')

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

            print('Gas: {0:.2f} Ohms,humidity: {1:.2f} %RH,air quality: {2:.2f},pressure: {3:.2f} hPa'.format(
                gas,
                hum,
                air_quality_score,
                pressure))

            write_data_to_influxdb(air_quality_score, gas, hum, pressure)
            time.sleep(5)

except KeyboardInterrupt:
    pass

client.close()