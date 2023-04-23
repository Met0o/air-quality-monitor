# Raspberry Pi 4 Air Quality Monitor System

Simple docker setup for a home-made PM 2.5 & PM 10, VOC, Co2, Temperature, and Humidity air quality monitoring system. 

This code is intended to work with Raspberry Pi 4 64bit OS, and the sensors SDS011, BME680 and M5Stack CO2L Unit (SCD41).

<pre>
```
project structure:
│   docker-compose.yml
|
└───air-voc-probe
|   |   Dockerfile
│   |   air-voc-probe.py
|
└───air-c02-temp-hum-probe
│   │   Dockerfile
│   │   air-c02-temp-hum-probe.py
|
└───air-quality-probe
│   │   Dockerfile
│   │   air-quality-probe.py
│
└───api_data
    │   Dockerfile
    │   api_data_fetch.py
```
</pre>

# Requirements (deployed as part of the Docker containers): 

  - Python 3.9 
    - pip packages: 
      - influxdb 
      - pyserial
      - tenacity
      - requests
      - smbus2
      - bme680
      - sensirion-i2c-sen5x
      - sensirion-i2c-scd

To install Docker on Raspberry Pi OS:

    - sudo curl -L "https://github.com/docker/compose/releases/download/v2.1.7/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    - sudo apt update
    - sudo apt install code

One specific to this implementation is the version of InfluxDB which for my setup is 1.8. Newer versions of influxdb enter in a reboot loop which I was unable to fix.  I've tried with containers from different architectures such as arm64v8 & arm32v7 and none of them worked.

The deployment spins up several microservices: 

  - InfluxDB
  - Grafana
  - Chronograf
  - Telegraf
  - Kapacitor
  - air-voc-probe
  - air-co2-temp-hum-probe
  - air-quality-probe
  - api-data-probe

air-voc-probe.py uses the BME680 Breakout - Air Quality, Temperature, Pressure, Humidity Sensor (https://shop.pimoroni.com/products/bme680-breakout) to append readings into influxDB in 5 second intervals.

air-co2-temp-hum-probe.py uses the M5Stack (https://shop.m5stack.com/products/co2l-unit-with-temperature-and-humidity-sensor-scd41) sensor to append readings into InfluxDB in 5 second intervals. 

air-quality-probe.py appends measurements from the SDS011 sensor into InfluxDB in 5 second intervals.

api-data-probe.py sources measurements from http://api.weatherapi.com/ and stores them into the InfluxDB container each 5 minutes. This data is used to compare the indoor with outdoor readings.

./conf folder contains the configuration plugins for telegraf and kapacitor (required only for the dashboards with system metrics). 

Setting up Chronograf dashboard requires some basic configuration from its GUI accessible at http://localhost:8888

# Latest Grafana dashboard
![Image description](./img/Grafana.png)

# Grafana dashboard with realtime reporting
![Image description](./img/grafana.png)

# Chronograf dashboard of the system utilization
![Image description](./img/chronograf.png)

# Chronograf dashboard with InfluxDB metrics
![Image description](./img/influxdb.png)
