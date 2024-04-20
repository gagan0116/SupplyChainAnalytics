import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from category_encoders import CountEncoder
from sklearn.preprocessing import OneHotEncoder,StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer

from src.logger import logging
from src.utils import save_obj
from src.exception import CustomException

@dataclass
class DataTransformationConfig:
    preprocessor_obj_filepath:str = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_transformation_object(self):
        try:
            logging.info("Creating Data Transormation Object")

            categorical_cols = ['Type' ,'Department Name', 'Order Region','Order Status', 
                                'Customer Segment']
            
            categorical_cols_high_cardinality = ['Product Name', 'Category Name', 'Order City', 
                                                 'Order Country', 'Customer Zipcode']

            numerical_cols = ['Benefit per order', 'Latitude', 'Longitude', 'Order Item Discount Rate', 
                              'Order Item Profit Ratio', 'Order Item Quantity', 'Sales', 'Product Price', 
                              'order_year', 'order_month', 'order_day']
            
            ordinal_cols = ['Shipping Mode']

            shipping_mode_cat = ['Same Day', 'First Class', 'Second Class', 'Standard Class']

            num_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())
            ])

            nominal_pipeline = Pipeline(
                steps=[
                ('imputer_nominal',SimpleImputer(strategy='most_frequent')),
                ('onehotencoder',OneHotEncoder(handle_unknown='ignore'))
            ])

            ordinal_pipeline = Pipeline(
                steps=[
                    ('imputer_ord',SimpleImputer(strategy='most_frequent')),
                    ('ordinalencoder',OrdinalEncoder(categories=[shipping_mode_cat])),
                    ('scaler_ord',StandardScaler())
                ]
            )

            cat_pipeline_high_cardinality= Pipeline(
                steps=[
                ('imputer_hicar',SimpleImputer(strategy='most_frequent')),
                ('countencoder',CountEncoder()),
                ('scaler',StandardScaler())
            ])

            preprocessor=ColumnTransformer([
            ('num_pipeline',num_pipeline,numerical_cols),
            ('nominal_pipeline',nominal_pipeline, categorical_cols),
            ('ordinal_pipeline', ordinal_pipeline, ordinal_cols),
            ('cat_pipeline_high_cardinality', cat_pipeline_high_cardinality, categorical_cols_high_cardinality)
            ])

            return preprocessor
            
            logging.info('Pipeline Initiated')

        except Exception as e:
            logging.info("Error Encountered while creating the Data Transformation Object")
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info('Read train and test data completed')

            logging.info('Obtaining preprocessing object')

            preprocessor_obj = self.get_transformation_object()

            target_cols = ['Days for shipping (real)', 'Days for shipment (scheduled)']

            input_feature_train_df = train_df.drop(columns=target_cols,axis=1)
            target_feature_train_df = train_df[target_cols]

            input_feature_test_df = test_df.drop(columns=target_cols,axis=1)
            target_feature_test_df = test_df[target_cols]

            logging.info("Applying preprocessing object on training and testing datasets.")

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            logging.info("Transformed Training and Testing Input Dataframes")

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_obj(
                file_path = self.data_transformation_config.preprocessor_obj_filepath,
                obj = preprocessor_obj
            )

            logging.info('Preprocessor pickle file saved')

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_filepath
            )

        except Exception as e:
            logging.info("Error Encountered while inintiating Data Transformation")
            raise CustomException(e, sys)