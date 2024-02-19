import psycopg2
from psycopg2 import sql
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

row_data_table_name = 'RowData2'
plant_data_table_name = 'PlantData2'

create_row_data_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {} (
        RowID INT PRIMARY KEY,
        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        AvgSoilPH FLOAT,
        AvgSoilMoisture FLOAT,
        AvgTemperature FLOAT,
        AvgHumidity FLOAT,
        AvgAirQuality FLOAT,
        Status VARCHAR(20)
    );
""").format(sql.Identifier(row_data_table_name))

create_plant_data_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {} (
        PlantID INT,
        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        RowID INT,
        PlantName VARCHAR(50) NOT NULL,
        SoilPH FLOAT NOT NULL,
        SoilMoisture FLOAT NOT NULL,
        Temperature FLOAT NOT NULL,
        Humidity FLOAT,
        AirQuality FLOAT,
        Status VARCHAR(20),
        PRIMARY KEY (PlantID, Timestamp),
        FOREIGN KEY (RowID) REFERENCES {}(RowID)
    );
""").format(sql.Identifier(plant_data_table_name), sql.Identifier(row_data_table_name))

try:
    connection = psycopg2.connect(**db_params)
    print("Connected to PostgreSQL!")

    cursor = connection.cursor()
    cursor.execute(create_row_data_table_query)
    cursor.execute(create_plant_data_table_query)
    connection.commit()
    print(f"Tables '{row_data_table_name}' and '{plant_data_table_name}' created successfully!")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection closed.")