import csv
import psycopg2
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
dbname = env_vars["DB_NAME"]
user = env_vars["DB_USER"]
password = env_vars["DB_PASSWORD"]
host = env_vars["DB_HOST"]
port = env_vars["DB_PORT"]


db_params = {
    'dbname': dbname, 
    'user': user,  
    'password': password, 
    'host': host,     
    'port': port              
}

conn = psycopg2.connect(**db_params)
cur = conn.cursor()
csv_file_path = "rowData2.csv"

with open(csv_file_path, newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        row_id = row['RowID']
        avg_soil_ph = row['AvgSoilPH']
        avg_soil_moisture = row['AvgSoilMoisture']
        avg_temperature = row['AvgTemperature']
        avg_humidity = row['AvgHumidity']
        avg_air_quality = row['AvgAirQuality']
        status = row['Status']
        
        cur.execute("""
            UPDATE public."RowData2"
            SET AvgSoilPH = %s, AvgSoilMoisture = %s, AvgTemperature = %s,
                AvgHumidity = %s, AvgAirQuality = %s, Status = %s
            WHERE RowID = %s
        """, (avg_soil_ph, avg_soil_moisture, avg_temperature,
              avg_humidity, avg_air_quality, status, row_id))

conn.commit()
cur.close()
conn.close()
