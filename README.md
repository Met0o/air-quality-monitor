# Raspberry Pi 4 and SDS011 air-quality-monitor

Simple docker setup for a home-made PM 2.5 & PM 10 air quality monitoring system. 

This code is intended to work with Raspberry Pi 4 and air quality sensor SDS011. 

Based on various blogposts, I find my approach the easiest to implement and with less constraints.

<pre>
```
project structure:
│   docker-compose.yml
│
└───air-quality-probe
│   │   Dockerfile
│   │   air-quality-probe.py
│
└───api_data
    │   Dockerfile
    │   api_data_fetch.py
```
</pre>

# Requirements: 

  - Python 3.9 
    - pip packages: 
      - influxdb 
      - pyserial
      - tenacity
      - requests

To install Docker on Raspberry Pi OS:
sudo curl -L "https://github.com/docker/compose/releases/download/v2.1.7/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

One specific to this implementation is the version of InfluxDB which for my setup is 1.8. Newer versions of influxdb enter in a reboot loop which I was unable to fix.  I've tried with containers from different architectures such as arm64v8 & arm32v7 and none of them worked.

The deployment spins up several microservices: 

  - InfluxDB
  - Grafana
  - Chronograf
  - Telegraf
  - Kapacitor
  - air-quality-probe
  - api-data-probe

air-quality-probe.py appends measurements from the SDS011 sensor into InfluxDB in 10 second intervals.

api-data-probe.py sources measurements from http://api.weatherapi.com/ and stores them into the InfluxDB container each 60 minutes. This data is used to compare the differences.

./conf folder contains the configuration plugins for telegraf and kapacitor (required only for the dashboards with system metrics). 

Setting up Chronograf dashboard requires some basic configuration from its GUI accessible at http://localhost:8888

# Grafana dashboard with realtime reporting
![Image description](./img/grafana.png)

# Chronograf dashboard of the system utilization
![Image description](./img/chronograf.png)

# Chronograf dashboard with InfluxDB metrics
![Image description](./img/influxdb.png)
