import csv
import psycopg2
from psycopg2 import sql
from datetime import datetime
import os
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

csv_file_path = './rowData2.csv'
table_name = 'RowData2'
insert_query = sql.SQL("""
    COPY {} (RowID, AvgSoilPH, AvgSoilMoisture, AvgTemperature, AvgHumidity, AvgAirQuality, Status)
    FROM STDIN
    WITH CSV HEADER DELIMITER ',' QUOTE '"';
""").format(sql.Identifier(table_name))

try:
    connection = psycopg2.connect(**db_params)
    print("Connected to PostgreSQL!")

    cursor = connection.cursor()
    with open(csv_file_path, 'r') as file:
        cursor.copy_expert(insert_query, file)
    connection.commit()
    print(f'Data from CSV file "{csv_file_path}" inserted into table "{table_name}" successfully!')
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL or inserting data:", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection closed.")


