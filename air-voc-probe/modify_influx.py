from influxdb import InfluxDBClient

# docker exec -it influxdb influx
# use bme680_data
# DROP MEASUREMENT bme680
# exit

client = InfluxDBClient(host='influxdb', port=8086)

# List available databases
databases = client.get_list_database()
for db in databases:
    print(db["name"])

# Drop the bme680_data
client.drop_database('bme680_data')
print("Database 'bme680_data' dropped.")

# Check again available databases
for db in databases:
    print(db["name"])