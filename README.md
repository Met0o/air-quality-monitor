# Raspberry Pi 4 and SDS011 air-quality-monitor

Simple docker setup with Raspberry Pi 4 for a home-made PM 2.5 & PM 10 air quality monitoring system. 

This code is intended to work with the sensor SDS011. 

Based on various blogposts, I find my approach the easiest to implement and with less constraints.

REquires Python 3.9 and pip packages - influxdb, pyserial, and tenacity.

One specific to this implementation is the version of InfluxDB which for my setup is 1.8. Newer versions of influxdb enter in a reboot loop which I was unable to fix.  I've tried with containers from different architectures such as amd64, arm64v8 & arm32v7 and regardless of the the architecture version, only 1.8 works.

This deployment containes several microservices including - InfluxDB, Grafana, Chronograf, Telegraf, Kapacitor, and an air-quality-probe.

air-quality-probe.py appends measurements from the SDS011 sensor into InfluxDB in 10 secon intervals.

./conf folder contains the configuration plugins for telegraf and kapacitor

Setting up Chronograf dashboard requires some basic configuration from its GUI accessible at http://localhost:8888

# Grafana dashboard with realtime reporting
![Image description](./img/grafana.png)

# Chronograf dashboard of the system utilization
![Image description](./img/chronograf.png)
