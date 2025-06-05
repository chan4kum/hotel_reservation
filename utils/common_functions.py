import os
import sys
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger= get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
        logger.info(f"Successfully read YAML file: {file_path}")
        return content
    except yaml.YAMLError as e:
        logger.error(f"Error reading YAML file {file_path}: {e}")
        raise CustomException(f"Error reading YAML file: {e}", sys) from e
    
def load_data(path):
    try:
        logger.info("Loading data from CSV file")
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        return pd.read_csv(path)
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        raise CustomException(f"Failed to load data: {path}", sys) from e
    except pd.errors.EmptyDataError as e:
        logger.error(f"Empty data error: {path}")
        raise CustomException(f"Empty data error: {path}", sys) from e
    except pd.errors.ParserError as e:
        logger.error(f"Parser error: {path}")
        raise CustomException(f"Parser error: {path}", sys) from e
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading data: {e}")
        raise CustomException(f"An unexpected error occurred: {e}", sys) from e