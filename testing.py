from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def divide_numbers(numerator, denominator):
    try:
        logger.info(f"Dividing {numerator} by {denominator}")
        result = numerator / denominator
        logger.info(f"Result: {result}")
        return result
    except ZeroDivisionError as e:
        logger.error(f"ZeroDivisionError: {e}")
        raise CustomException("Denominator cannot be zero", sys) from e
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise CustomException("An unexpected error occurred", sys) from e
    

if __name__ == "__main__":
    try:
        logger.info("Starting the division operation")
        result = divide_numbers(10, 0)  # This will raise a ZeroDivisionError
    except CustomException as e:
        logger.error(f"CustomException: {e}")