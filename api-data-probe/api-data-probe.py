import requests
import time
import json
import os

API_KEY = 'ae3fd22b40dd4b6295685733232603'
WEATHER_API_URL = 'http://api.weatherapi.com/v1/current.json'
INTERNAL_API_BASE = os.environ.get("API_BASE", "http://localhost:8000")
INTERNAL_API_URL = f"{INTERNAL_API_BASE}/ingest/weather"

while True:
    try:
        response = requests.get(WEATHER_API_URL, params={'key': API_KEY, 'q': 'Sofia', 'aqi': 'yes'})
        data = response.json()

        location = data['location']
        current = data['current']
        
        payload = {
            'location': location['name'],
            'region': location['region'],
            'country': location['country'],
            'temperature': current['temp_c'],
            'humidity': current['humidity'],
            'wind_speed': current['wind_kph'],
            'air_quality_co': current['air_quality']['co'],
            'air_quality_no2': current['air_quality']['no2'],
            'air_quality_o3': current['air_quality']['o3'],
            'air_quality_so2': current['air_quality']['so2'],
            'air_quality_pm2_5': current['air_quality']['pm2_5'],
            'air_quality_pm10': current['air_quality']['pm10'],
            'localtime': location['localtime']
        }
        
        internal_response = requests.post(INTERNAL_API_URL, json=payload, timeout=5)
        print(f'Weather data sent to internal API: {payload["location"]}, {payload["temperature"]}°C')
        
    except Exception as e:
        print('Error fetching or sending weather data:', e)
    
    time.sleep(1)
