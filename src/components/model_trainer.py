import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score

from src.logger import logging
from src.exception import CustomException
from src.utils import save_obj, evaluate_models

@dataclass 
class ModelTrainerConfig():
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTraining:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_arr, test_arr):
        try:
            logging.info("Splitting training and test input data")

            X_train, y_train = (train_arr[:,:-2], train_arr[:,-2:])
            X_test, y_test = (test_arr[:,:-2], test_arr[:,-2:])

            models = {                
                "Linear Regression": LinearRegression(),
                "Ridge": Ridge(), 
                "Lasso":Lasso(), 
                "Decision Tree": DecisionTreeRegressor(),
                "XGBRegressor": XGBRegressor(),
                "K Neighbors Regressor": KNeighborsRegressor()
                }
            
            params = {
                "Decision Tree": {
                    'criterion':['squared_error','friedman_mse'],
                },
                "Linear Regression":{
                },
                "Ridge":{
                    'alpha': [0.01, 0.1, 1.0, 10.0]
                },
                "Lasso":{
                    'alpha': [0.01, 0.1, 1.0, 10.0]
                },
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                     'n_estimators': [8,16,32,64,128,256]
                },
                "K Neighbors Regressor": {
                    'n_neighbors': [3, 5, 10, 20],
                    'weights': ['uniform', 'distance']
                },
                
            }

            model_report:dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, params = params)
            logging.info(f"The Model report is: \n{model_report}")
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            logging.info(f"The best model is:{best_model_name}")

            best_model = models[best_model_name]

            if best_model_score < 0.7:
                raise CustomException("No best Model Found")
            logging.info(f"Best found model on both training and testing daataset")

            save_obj(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)

            return r2_square

        except Exception as e:
            raise CustomException(e, sys)