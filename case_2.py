import os
from dotenv import load_dotenv

import mysql.connector
import pandas as pd
import datetime

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

if __name__ == "__main__":
    load_dotenv()
    try:
        connection = connect_to_db()
    except: 
        print("Error connecting to the database.")
        connection = None
    
    query1 = '''
    SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
    FROM data_store_cad 
    '''
    
    query2 = '''
    SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
    FROM data_store_sales
    WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
    '''
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query1)
    store_cad_df = pd.DataFrame(cursor.fetchall())
    cursor.execute(query2)
    store_sales_df = pd.DataFrame(cursor.fetchall())
    
    cursor.close()
    connection.close()
    
    store_info_full = pd.merge(store_cad_df, store_sales_df, how='left')
    
    # Nesta parte, foi utilizada a resposta de IA do Google apenas para corrigir a sintaxe do método "between", que eu não utilizo frequentemente
    data_view = store_info_full[store_info_full['DATE'].between(datetime.date(2019,10,1), datetime.date(2019,12,31))] \
        .groupby(['STORE_NAME', 'BUSINESS_NAME']) \
        .sum(['SALES_VALUE', 'SALES_QTY']) \
        .eval('TM = SALES_VALUE / SALES_QTY')['TM'] \
        .round(2)
    print(data_view)
    