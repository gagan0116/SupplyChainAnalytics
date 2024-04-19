import os
import sys
from dotenv import load_dotenv
import mysql.connector as connection
from sqlalchemy import create_engine
import pandas as pd
import pickle

from src.exception import CustomException
from src.logger import logging

def sqlalchemy_connection(database_name):
    try:
        load_dotenv()
        sqlpassword = os.getenv('SQL_PASSWORD')
        logging.info("Retrieved SQL Password from .ENV File")
        engine = create_engine(f'mysql+mysqlconnector://root:{sqlpassword}@localhost/{database_name}')
        logging.info("Created SQL Alchemy Engine Successfully with connection to database SupplyChainData")

        return engine

    except Exception as e:
        logging.info("Error occured in SQL connection Establishment in utils")
        raise CustomException(e,sys)
    
    else:
        logging.info("Connection to SQL established successfully")


def extract_data_from_sql(database_name, table_name):
    try:
        engine = sqlalchemy_connection(database_name)
        con = engine.connect()
        logging.info("Retrieved the SQL Alchemy Engine")

        df = pd.read_sql_table(table_name, con=con)
        logging.info("Completed Reading the SQL Table")

        data_path = os.path.join("notebooks", "data", "supplychaindata.csv")
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        
        df.to_csv(data_path, index=False)
        logging.info("Stored the dataset as a csv file")

    except Exception as e:
        logging.info("Error occured while Extracting Data from SQL in utils")
        raise CustomException(e,sys)
    
    else:
        logging.info("Successfully extracted data from SQL and stored.")

def load_obj(file_path):
    try: 
        with open(file_path, 'rb') as file_obj: 
            return pickle.load(file_obj)
    except Exception as e: 
        logging.info("Error in load_object fuction in utils")
        raise CustomException(e,sys)
    
def save_obj(file_path, obj): 
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok= True)
    with open (file_path, "wb") as file_obj: 
        pickle.dump(obj, file_obj)





