import os
import sys
import pandas as pd
import numpy as np

from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
    def preprocess_data(self,df):
        try:
            logger.info("Starting data preprocessing")

            logger.info("Dropping the columns")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'],inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]
            logger.info(f"Categorical columns: {cat_cols}")
            logger.info(f"Numerical columns: {num_cols}")
            logger.info("Applying Label Encoding")

            label_encoder = LabelEncoder()
            mappings = {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label,code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}

            logger.info("Label Encoding Mapping are: ")
            for col,mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info("Handling skewness in numerical columns")

            skew_threshold = self.config["data_processing"]["skew_threshold"]

            skewness = df[num_cols].apply(lambda x: x.skew())

            for column in skewness[skewness > skew_threshold].index:
                df[column]= np.log1p(df[column])
            
            logger.info("Skewness handled")

            return df


        except Exception as e:
            logger.error(f"Error in preprocessing data: {e}")
            raise CustomException("Error while preprocess data",e)
        


    def balance_data(self,df):
        try:
            logger.info("Balancing data using SMOTE")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled

            logger.info("Data balanced successfully")
            return balanced_df

        except Exception as e:
            logger.error(f"Error in balancing data: {e}")
            raise CustomException("Error while balancing data",e)
        
    def select_features(self,df):
        try:
            logger.info("Starting our Feature Selectiion process")

            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]
            logger.info(f"qwweewqe Shape of features: {X.shape}, Shape of target: {y.shape}")

            model = RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance=model.feature_importances_

            feature_importance_df = pd.DataFrame({
                            'feature':X.columns,
                            'importance':feature_importance
                        })
            top_featuresf_importance_df=feature_importance_df.sort_values(by='importance', ascending=False )

            num_features_to_select = self.config["data_processing"]["no_of_features"]

            top_10_features = top_featuresf_importance_df["feature"].head(num_features_to_select).values
            top_10_df = df[top_10_features.tolist() + ["booking_status"]]
            logger.info(f"Top {num_features_to_select} features selected based on importance: {top_10_features}")

            logger.info(f"hhfhhfhffhjhj Top {num_features_to_select} features selected: {top_10_df}")

            return top_10_df
        
        except Exception as e:
            logger.error(f"Error in selecting feature data: {e}")
            raise CustomException("Error while feature selection",e)
        

    def save_data(self,df,file_path):
        try:
            logger.info(f"Saving our data in processed folder at {file_path}")
            df.to_csv(file_path, index=False)
            logger.info("Data saved successfully")
        except Exception as e:
            logger.error(f"Error in saving data: {e}")
            raise CustomException("Error while saving data",e)
        
    def process(self):
        try:
            logger.info("Loading the data from raw directory")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            logger.info("Data loaded successfully")
            logger.info(f"1Shape of features: {train_df.shape}, 1Shape of target: {test_df.shape}")
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)
            logger.info(f"2Shape of features: {train_df.shape}, 2Shape of target: {test_df.shape}")
            logger.info("Data preprocessing completed")

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)
            logger.info("Data balancing completed")
            logger.info(f"3Shape of features: {train_df.shape}, 3Shape of target: {test_df.shape}")

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]
            logger.info("Feature selection completed")
            logger.info(f"4Shape of features: {train_df.shape}, 4Shape of target: {test_df.shape}")

            self.save_data(train_df,PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)
            logger.info("Data processing completed successfully")
        except Exception as e:
            logger.error(f"Error in data processing: {e}")
            raise CustomException("Error while processing data", e)
if __name__ == "__main__":
    try:
        processor = DataProcessor(
            train_path=TRAIN_FILE_PATH,
            test_path=TEST_FILE_PATH,
            processed_dir=PROCESSED_DIR,
            config_path=CONFIG_PATH
        )
        processor.process()
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        sys.exit(1)



