# air-quality-monitor

Simple docker setup for Raspberry Pi 4 for a home-made PM 2.5 & PM 10 air quality monitoring system. 

This code is intended to work with sensor SDS011. 

Based on various guides, I find my approach the easiest to implement and with less constraints.

Python dependencies are Python 3.9, and these 3 pip packages - influxdb, pyserial, and tenacity.

One specific to this implementation is the version of InfluxDB which for my setup appears to be 1.8. Newer versions of influxdb enter in a reboot loop which I was unable to fix that.

Docker-compose.yml contains all interdependencies and settings.
