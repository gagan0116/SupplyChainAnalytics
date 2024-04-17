from src.logger import logging
from src.exception import CustomException
from src.utils import extract_data_from_sql

if __name__ == "__main__":
    database = "SupplyChainData"
    table = "supplychain"
    extract_data_from_sql(database_name=database, table_name=table)