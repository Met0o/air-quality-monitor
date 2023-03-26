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

One specific to this implementation is the version of InfluxDB which for my setup is 1.8. Newer versions of influxdb enter in a reboot loop which I was unable to fix.  I've tried with containers from different architectures such as amd64, arm64v8 & arm32v7 and regardless of the the architecture version, only influxdb 1.8 works.

The deployment containes several microservices including: 
  - InfluxDB
  - Grafana
  - Chronograf
  - Telegraf
  - Kapacitor
  - air-quality-probe

air-quality-probe.py appends measurements from the SDS011 sensor into InfluxDB in 10 secon intervals.

./conf folder contains the configuration plugins for telegraf and kapacitor (required only for the dashboards with system metrics)

Setting up Chronograf dashboard requires some basic configuration from its GUI accessible at http://localhost:8888

# Grafana dashboard with realtime reporting
![Image description](./img/grafana.png)

# Chronograf dashboard of the system utilization
![Image description](./img/chronograf.png)

# Chronograf dashboard with InfluxDB metrics
![Image description](./img/influxdb.png)
