# Raspberry Pi 4 Air Quality Monitor

Dockerized home air‑quality stack for PM2.5/PM10 (SDS011), VOC/Temp/Pressure/Humidity (BME680), CO₂/Temp/Humidity (SCD41), and multi‑gas (Grove MGS V2). Time‑series are kept in memory via a sliding window API (no InfluxDB), and visualized in Grafana using the Infinity datasource.

This project targets Raspberry Pi 4 (64‑bit OS) with I²C enabled.

## What’s in here

- API (`FastAPI`): in‑memory sliding window store with retention
- Probes: read sensors and POST to the API every 10s
  - `air-quality-probe` (SDS011, serial `/dev/ttyUSB0`)
  - `air-voc-probe` (BME680, I²C `/dev/i2c-1`)
  - `air-co2-temp-hum-probe` (SCD41, I²C `/dev/i2c-1`)
  - `air-co-voc-no2-c2h5oh-probe` (Grove MGS V2, I²C `/dev/i2c-1`)
  - `api-data-probe` (WeatherAPI reference data)
- Grafana: dashboards via Infinity datasource

## Project structure

```
compose.yml
Dockerfile (API image)
main.py (API)
air-quality-probe/
air-voc-probe/
air-co2-temp-hum-probe/
air-co-voc-no2-c2h5oh-probe/
api-data-probe/
dashboards/
img/
```

## Install Docker on Raspberry Pi OS

- `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`
- Reboot or add user to docker group

## Run

```
sudo docker compose up -d --build
```

- Grafana: http://localhost:3000 (user: `admin`, pass: `admin`)
- API: http://localhost:8000

The compose file installs the Grafana Infinity plugin automatically.

## API

- `POST /ingest/{measurement}`: append a data point
- `GET  /query/{measurement}`: return current sliding window as JSON

Measurements used by the probes:

- `sds011` (PM2.5/PM10)
- `bme680` (gas_resistance, humidity, pressure, temp, optional air_quality_score after calibration)
- `scd4x` (co2_ppm, temperature_c, humidity_rh)
- `groove_mgs_v2` (NO2, C2H5OH, VOC, CO)
- `weather` (temperature, humidity, wind, and AQ fields)

Example:

```bash
curl -s http://localhost:8000/query/bme680 | jq '.[-3:]'
```

Retention is enforced in memory on every ingest. Default is 24h and is configurable via `RETENTION_SECONDS`.

## Configuration (env)

Set in `compose.yml`:

- API
  - `RETENTION_SECONDS` (default `86400`)
- Probes
  - `API_BASE` (default inside containers `http://api:8000`)
- Weather probe
  - `WEATHER_API_KEY` (required)
  - `WEATHER_INTERVAL_SECONDS` (default `300`)

All services have Docker log rotation enabled (`json-file`, `10m` x `3`) to protect SD card space.

## Notes on sensors

- BME680 air quality score: the IAQ value is emitted after a calibration burn‑in. Default burn‑in is ~100 cycles at 10s each (~17 minutes). Before that, only gas/humidity/pressure/temp are posted.
- Devices required by containers:
  - `/dev/ttyUSB0` for SDS011
  - `/dev/i2c-1` for I²C sensors

## Grafana

- Uses the Infinity datasource to query the API directly (no time‑series DB).
- Dashboards can be imported from `dashboards/`.

## SD‑card considerations

- API stores data in memory only; `tmpfs` is used for ephemeral paths.
- Grafana persists minimal metadata in `grafana-storage` (SQLite DB, dashboards, plugins). This is small and bounded relative to usage; not a time‑series store.
- Docker logs are rotated/capped.

## Troubleshooting

- No IAQ score on BME680 panels right after startup: wait for calibration to finish, or check `bme680` container logs.
- Check API quickly: `curl -s http://localhost:8000/`.

## Hardware and libraries

- SDS011, BME680, SCD41, Grove MGS V2
- Python libs are installed inside each container during build (no host Python setup needed).

## Screenshot

![Grafana](./img/Grafana2023-07-13.png)