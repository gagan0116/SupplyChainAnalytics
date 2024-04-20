import sys 
import os 
import pandas as pd

from src.exception import CustomException 
from src.logger import logging 
from src.utils import load_obj

class PredictPipeline: 
    def __init__(self) -> None:
        pass

    def predict(self, features): 
        try: 
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            model_path = os.path.join("artifacts", "model.pkl")

            preprocessor = load_obj(preprocessor_path)
            model = load_obj(model_path)

            data_scaled = preprocessor.transform(features)
            pred = model.predict(data_scaled)
            return pred
        except Exception as e: 
            logging.info("Error occured in predict function in prediction_pipeline location")
            raise CustomException(e,sys)
        
class CustomData: 
        def __init__(self, Benefit_per_order:float, 
                     Latitude:float, 
                     Longitude:float, 
                     Order_Item_Discount_Rate:float, 
                     Order_Item_Profit_Ratio:float, 
                     Order_Item_Quantity:int, 
                     Sales:float, 
                     Product_Price:float, 
                     order_year:int,
                     order_month:int,
                     order_day:int,
                     Type:str,
                     Department_Name:str,
                     Order_Region:str,
                     Order_Status:str,
                     Customer_Segment: str,
                     Shipping_Mode: str,
                     Product_Name: str,
                     Category_Name: str,
                     Order_City: str,
                     Order_Country:str,
                     Customer_Zipcode: str): 
             self.Benefit_per_order = Benefit_per_order
             self.Latitude = Latitude
             self.Longitude = Longitude
             self.Order_Item_Discount_Rate = Order_Item_Discount_Rate
             self.Order_Item_Profit_Ratio = Order_Item_Profit_Ratio 
             self.Order_Item_Quantity = Order_Item_Quantity
             self.Sales = Sales 
             self.Product_Price = Product_Price 
             self.order_year = order_year
             self.order_month = order_month
             self.order_day = order_day
             self.Type = Type
             self.Department_Name = Department_Name
             self.Order_Region = Order_Region
             self.Order_Status = Order_Status
             self.Customer_Segment = Customer_Segment
             self.Shipping_Mode = Shipping_Mode
             self.Product_Name = Product_Name
             self.Category_Name = Category_Name
             self.Order_City = Order_City
             self.Order_Country = Order_Country
             self.Customer_Zipcode = Customer_Zipcode

        
        def get_data_as_dataframe(self): 
             try: 
                  custom_data_input_dict = {
                       'Benefit per order': [self.Benefit_per_order], 
                       'Latitude': [self.Latitude], 
                       'Longitude': [self.Longitude], 
                       'Order Item Discount Rate': [self.Order_Item_Discount_Rate],
                       'Order Item Profit Ratio':[self.Order_Item_Profit_Ratio],
                       'Order Item Quantity':[self.Order_Item_Quantity], 
                       'Sales': [self.Sales], 
                       'Product Price': [self.Product_Price], 
                       'order_year': [self.order_year],
                       'order_month': [self.order_month],
                       'order_day': [self.order_day],
                       'Type': [self.Type],
                       'Department Name': [self.Department_Name],
                       'Order Region': [self.Order_Region],
                       'Order Status': [self.Order_Status],
                       'Customer Segment': [self.Customer_Segment],
                       'Shipping Mode': [self.Shipping_Mode],
                       'Product Name': [self.Product_Name],
                       'Category Name': [self.Category_Name],
                       'Order City': [self.Order_City],
                       'Order Country': [self.Order_Country],
                       'Customer Zipcode': [self.Customer_Zipcode]

                  }
                  df = pd.DataFrame(custom_data_input_dict)
                  logging.info("Dataframe created")
                  return df
             except Exception as e:
                  logging.info("Error occured in get_data_as_dataframe function in prediction_pipeline")
                  raise CustomException(e,sys) 