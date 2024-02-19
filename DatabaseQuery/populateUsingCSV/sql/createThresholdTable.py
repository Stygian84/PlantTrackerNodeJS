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


conn = psycopg2.connect(**db_params)   
cursor = conn.cursor()
create_table_query = '''
    CREATE TABLE SoilProperties (
        id SERIAL PRIMARY KEY,
        property_name VARCHAR(50),
        value FLOAT,
        good_threshold FLOAT,
        moderate_threshold FLOAT,
        bad_threshold FLOAT
    )
'''

cursor.execute(create_table_query)

data = [
    ('soilph', 6.5, 0.3, 1.0, 2.0),
    ('soilmoisture', 30, 8, 12, 18),
    ('temperature', 30, 10, 15, 20),
    ('humidity', 80, 10, 15, 20),
    ('airquality', 0, 50, 100, 200)
]

insert_query = '''
    INSERT INTO SoilProperties 
    (property_name, value, good_threshold, moderate_threshold, bad_threshold) 
    VALUES (%s, %s, %s, %s, %s)
'''
cursor.executemany(insert_query, data)
conn.commit()
cursor.close()
conn.close()
