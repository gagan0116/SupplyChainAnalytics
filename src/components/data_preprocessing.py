import os
import sys
from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException

# Dataclass decorator automatically initialises the data variables.
@dataclass
class DataPreprocessConfig:
    train_data_path:str = os.path.join('artifacts', 'train.csv')
    test_data_path:str = os.path.join("artifacts", "test.csv")
    raw_data_path:str = os.path.join("artifacts", "raw.csv")

class DataPreprocess:
    def __init__(self):
        self.preprocess_config = DataPreprocessConfig()
    
    def initiate_data_preprocess(self):
        logging.info("Initialising the Data Preprocessing...")
        try:
            df = pd.read_csv(os.path.join('notebooks/data', 'supplychaindata.csv'))
            logging.info('Dataset read as pandas Dataframe')

            prim_drop_col = ["Product Description", "Order Zipcode", "Customer Lname", "Product Image", "Customer Email", 
            "Customer Fname", "Customer Password", "Customer Street", "Order Id", "Customer City", 
             "Customer State", "Customer Country", "Customer Id"]

            df.drop(columns=prim_drop_col, inplace=True)
            logging.info("Dropped Unncessary Columns")

            df.dropna(inplace = True)
            logging.info("Dropped Null Values from the dataset")

            df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
            df['shipping date (DateOrders)'] = pd.to_datetime(df['shipping date (DateOrders)'])\
            
            df['order_year'] = pd.DatetimeIndex(df['order date (DateOrders)']).year
            df['order_month'] = pd.DatetimeIndex(df['order date (DateOrders)']).month
            df['order_day'] = pd.DatetimeIndex(df['order date (DateOrders)']).day
            df['shipping_year'] = pd.DatetimeIndex(df['shipping date (DateOrders)']).year
            df['shipping_month'] = pd.DatetimeIndex(df['shipping date (DateOrders)']).month
            df['shipping_day'] = pd.DatetimeIndex(df['shipping date (DateOrders)']).day

            logging.info("Feature Engineering completed for DateTime columns")

            unwanted_cols = ["Order Profit Per Order", "Sales per customer", "Order Item Total", 
                             "Order Item Product Price", "Product Status", "Order Item Cardprod Id", 
                             "Product Category Id", "Product Card Id",  "Department Id", 
                             "Order Customer Id", "shipping date (DateOrders)", "order date (DateOrders)", 
                             "Order Item Discount", "Delivery Status", "Late_delivery_risk", 
                             "Category Id", "Order Item Id", "Market", "Order State"]

            df.drop(columns=unwanted_cols, inplace=True)

            df["Customer Zipcode"] = df["Customer Zipcode"].astype(str)
            df["Customer Zipcode"] = df["Customer Zipcode"].str.split('.').str[0]

            logging.info("Modified the Data Type of column Customer ZipCode")

            os.makedirs(os.path.dirname(self.preprocess_config.raw_data_path),exist_ok=True)
            df.to_csv(self.preprocess_config.raw_data_path,index=False)

            logging.info('Initialising Train test split')

            train_set,test_set = train_test_split(df,test_size=0.30,random_state=42)
            train_set.to_csv(self.preprocess_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.preprocess_config.test_data_path,index=False,header=True)

            logging.info('Preprocessing of Data is completed')
            
            return (
                self.preprocess_config.train_data_path,
                self.preprocess_config.test_data_path
            )

        except Exception as e:
            logging.info("An Exception Occured while Performing Data Preprocessing Component")
            raise CustomException(e, sys)
        

