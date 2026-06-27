import os
from dotenv import load_dotenv

import mysql.connector
import pandas as pd

def connect_to_db():
    
    host = os.getenv("HOST")
    username = os.getenv("USER")
    password = os.getenv("PASSWORD")
    schema = os.getenv("SCHEMA")
    
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=schema
    )
    
    if connection.is_connected():
        print("Connection to the database was successful!")
        return connection
    else:
        print("Failed to connect to the database.")
        return None

def retrieve_data(product_code: int, store_code: int, date: list):
    load_dotenv()
    try:
        connection = connect_to_db()
    except: 
        print("Error connecting to the database.")
        return None
    
    cursor = connection.cursor(dictionary=True)
    
    # Abordagem por datas individuais
    query = f'''
        SELECT * 
        FROM data_product_sales dps 
        WHERE CAST(dps.DATE AS CHAR(10)) IN {date}
        AND dps.store_code = {store_code}
        AND dps.product_code = {product_code}
        '''.replace('[', '(').replace(']', ')')
    try:
        cursor.execute(query)
        dataframe = cursor.fetchall()
    except:
        print('Error executing query!')
        cursor.close()
        connection.close()
        raise
    
    cursor.close()
    connection.close()
    return pd.DataFrame(dataframe)
    
    


if __name__ == "__main__":
    my_data = retrieve_data(product_code=18, store_code=1, date=['2019-01-01', '2019-01-31']) # Example
    print(my_data)