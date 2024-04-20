from src.components.data_preprocessing import DataPreprocess
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTraining
from src.logger import logging

if __name__ == '__main__':
    preprocess_obj = DataPreprocess()
    train_data_path, test_data_path = preprocess_obj.initiate_data_preprocess()
    transformation_obj = DataTransformation()
    train_arr, test_arr, _ = transformation_obj.initiate_data_transformation(train_data_path, test_data_path)
    trainer_obj = ModelTraining()
    r2score = trainer_obj.initiate_model_trainer(train_arr, test_arr)
    logging.info(f"The r2 score is: {r2score}")