import requests
import time
import json

API_KEY = 'ae3fd22b40dd4b6295685733232603'
API_URL = 'http://api.weatherapi.com/v1/current.json'


#API_URL = 'http://api.weatherapi.com/v1/forecast.json'

# while True:
#     try:
#         response = requests.get(API_URL, params={'key': API_KEY, 'q': 'Sofia', 'aqi': 'yes'})
#         data = response.json()

#         location = data['location']
#         current = data['current']
        
#         tags = {
#             'location': location['name'],
#             'region': location['region'],
#             'country': location['country']
#         }
        
#         fields = {
#             'temperature': current['temp_c'],
#             'humidity': current['humidity'],
#             'wind_speed': current['wind_kph'],
#             'air_quality_co': current['air_quality']['co'],
#             'air_quality_no2': current['air_quality']['no2'],
#             'air_quality_o3': current['air_quality']['o3'],
#             'air_quality_so2': current['air_quality']['so2'],
#             'air_quality_pm2_5': current['air_quality']['pm2_5'],
#             'air_quality_pm10': current['air_quality']['pm10']
#         }
        
#         timestamp = int(location['localtime_epoch']) * 1000000000
        
#         json_body = [
#             {
#                 'measurement': 'weather',
#                 'tags': tags,
#                 'time': timestamp,
#                 'fields': fields
#             }
#         ]
#     except Exception as e:
#         print('Error:', e)
    
#     time.sleep(2)
    
    
response = requests.get(API_URL, params={'key': API_KEY, 'q': 'Sofia', 'aqi': 'yes'})
data = response.json()

location = data['location']
current = data['current']

tags = {
    'location': location['name'],
    'region': location['region'],
    'country': location['country']
}

fields = {
    'temperature': current['temp_c'],
    'humidity': current['humidity'],
    'wind_speed': current['wind_kph'],
    'air_quality_co': current['air_quality']['co'],
    'air_quality_no2': current['air_quality']['no2'],
    'air_quality_o3': current['air_quality']['o3'],
    'air_quality_so2': current['air_quality']['so2'],
    'air_quality_pm2_5': current['air_quality']['pm2_5'],
    'air_quality_pm10': current['air_quality']['pm10']
}