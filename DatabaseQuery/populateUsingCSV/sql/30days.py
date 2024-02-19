import csv
import random
from datetime import datetime, timedelta
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

def calculate_overall_status(avg_values):
    criteria = {
        "AvgSoilPH": {"good": [6.2, 6.8], "moderate": [5.5,7.5], "bad": [-float("inf"), 6.0, 8.0, float("inf")]},
        "AvgSoilMoisture": {"good": [22, 38], "moderate": [18,42], "bad": [-float("inf"), 20, 60, float("inf")]},
        "AvgTemperature": {"good": [20, 40], "moderate": [15, 45], "bad": [-float("inf"), 15, 35, float("inf")]},
        "AvgHumidity": {"good": [70,90], "moderate": [65,95], "bad": [-float("inf"), 40, 80, float("inf")]},
        "AvgAirQuality": {"good": [50], "moderate": [100], "bad": [-float("inf"), 70, 95, float("inf")]}
    }

    status = {"good": True, "moderate": False, "bad": False}

    for param, ranges in criteria.items():
        value = avg_values[list(criteria.keys()).index(param)]  
        if (param=="AvgAirQuality"):
            if value <= ranges["good"][0]:
                status["good"] = True
                status["moderate"] = False
                status["bad"] = False
            if ranges["good"][0]<=value<=ranges["moderate"][0]:
                status["good"] = False
                status["moderate"] = True
                status["bad"] = False
            if value >= ranges["moderate"][0]:
                status["good"] = False
                status["moderate"] = False
                status["bad"] = True
        else:
            if ranges["good"][0] <=value<= ranges["good"][1]:
                status["good"] = True
                status["moderate"] = False
                status["bad"] = False
            if (ranges["good"][0]<=value<=ranges["moderate"][0]) or (ranges["good"][1]<=value<=ranges["moderate"][1]):
                status["good"] = False
                status["moderate"] = True
                status["bad"] = False
            if (value <= ranges["moderate"][0]) or( value >= ranges["moderate"][1]):
                status["good"] = False
                status["moderate"] = False
                status["bad"] = True

    if status["good"]:
        return "Good"
    elif status["moderate"]:
        return "Moderate"
    elif status["bad"]:
        return "Bad"

    return "Undefined"
plant_names = ["carrot", "potatoes", "tomato", "lettuce", "cucumber", "spinach", "pepper", "onion", "radish", "corn", "eggplant", "bean"]


# Create 180 days past data for 12 rows which has 12 plants each
for day in range(180):
    days_ago=day
    plant_data = [
        ["PlantID", "Timestamp","RowID", "PlantName", "SoilPH", "SoilMoisture", "Temperature", "Humidity", "AirQuality","Status"],
    ]
    unique_plant_id_tracker = {}
    for row_id in range(1, 13):  
        for plant_id in range(1, 13):  
            plant_name = f"Plant{chr(64 + plant_id)}" 
            plant_name = plant_names[plant_id-1].capitalize()  
            soil_ph = round(random.uniform(5.5, 7.5) ,1) 
            soil_moisture = round(random.uniform(20,40) ,1)  
            temperature = round(random.uniform(20,40) ,1)  
            humidity = round(random.uniform(70,90) ,1)  
            air_quality = round(random.uniform(0,100) ,1)  
            timestamp = (datetime.now() - timedelta(days=days_ago))
            milliseconds = random.randint(0, 999)
            timestamp_with_ms = (timestamp + timedelta(milliseconds=milliseconds)).strftime('%Y-%m-%d %H:%M:%S')
    
            plant_key = (row_id, plant_name)
            if plant_key not in unique_plant_id_tracker:
                unique_plant_id_tracker[plant_key] = len(unique_plant_id_tracker) + 1
            unique_plant_id = unique_plant_id_tracker[plant_key]

            
            plant_entry = [unique_plant_id,timestamp, row_id, plant_name, soil_ph, soil_moisture, temperature, humidity, air_quality]

            
            avg_values = plant_entry[4:]  
            overall_status = calculate_overall_status(avg_values)
            plant_entry.append(overall_status)

            plant_data.append(plant_entry)

    
    row_data = [
    ["RowID", "AvgSoilPH", "AvgSoilMoisture", "AvgTemperature", "AvgHumidity", "AvgAirQuality","Status"],
]
    

    row_id_data = {}

    unique_plant_id_tracker = {}

    
    for plant_entry in plant_data[1:]:
        plant_id,timestamp, row_id, plant_name, soil_ph, soil_moisture, temperature, humidity, air_quality, status= plant_entry

        plant_key = (row_id, plant_name)
        if plant_key not in unique_plant_id_tracker:
            unique_plant_id_tracker[plant_key] = len(unique_plant_id_tracker) + 1

        unique_plant_id = unique_plant_id_tracker[plant_key]

        if row_id not in row_id_data:
            row_id_data[row_id] = {
                "SoilPH": 0,
                "SoilMoisture": 0,
                "Temperature": 0,
                "Humidity": 0,
                "AirQuality": 0,
                "Count": 0
            }

        row_id_data[row_id]["SoilPH"] += soil_ph
        row_id_data[row_id]["SoilMoisture"] += soil_moisture
        row_id_data[row_id]["Temperature"] += temperature
        row_id_data[row_id]["Humidity"] += humidity
        row_id_data[row_id]["AirQuality"] += air_quality
        row_id_data[row_id]["Count"] += 1

        
        plant_entry[0] = unique_plant_id

    
    for row_id in row_id_data:
        avg_values = [
            row_id,
            round(row_id_data[row_id]["SoilPH"] / row_id_data[row_id]["Count"], 1),
            round(row_id_data[row_id]["SoilMoisture"] / row_id_data[row_id]["Count"], 1),
            round(row_id_data[row_id]["Temperature"] / row_id_data[row_id]["Count"], 1),
            round(row_id_data[row_id]["Humidity"] / row_id_data[row_id]["Count"], 1),
            round(row_id_data[row_id]["AirQuality"] / row_id_data[row_id]["Count"], 1),
        ]

        
        overall_status = calculate_overall_status(avg_values[1:])
        avg_values.append(overall_status)

        row_data.append(avg_values)


    csv_file_path = "plantData2.csv"

    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(plant_data)
    
    csv_file_path = "rowData2.csv"

    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(row_data)

    print(f'CSV file "{csv_file_path}" created successfully.')
    csv_file_path = './plantData2.csv'
    table_name = 'PlantData2'




    
    
    


    insert_query = sql.SQL("""
        COPY {} (PlantID,Timestamp, RowID, PlantName, SoilPH, SoilMoisture, Temperature, Humidity, AirQuality, Status)
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
        print(f'Data from CSV file "{csv_file_path}" Day "{day}" inserted into table "{table_name}" successfully!')

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or inserting data:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection closed.")

    

