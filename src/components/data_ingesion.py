import os
import sys

import pandas as pd

from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
from src.logger import logger
from src.exception import CustomException
logger.info("i am working")

@dataclass
class DataIngestionConfig:
    """
    Stores all paths related to data ingestion.
    """

    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw.csv")


class DataIngestion:
    """
    Handles loading dataset and splitting into train and test sets.
    """

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self, file_path):
        """
        Reads dataset, stores raw data,
        splits into train and test,
        and saves the results.

        Parameters
        ----------
        file_path : str
            Path of the input csv file.

        Returns
        -------
        tuple
            (train_data_path, test_data_path)
        """

        logger.info("Entered Data Ingestion Component")

        try:

            # Reading Dataset
            logger.info("Reading dataset from %s", file_path)

            df = pd.read_csv(file_path)

            logger.info(
                "Dataset Loaded Successfully | Rows: %d | Columns: %d",
                df.shape[0],
                df.shape[1],
            )

            # Create artifacts folder
            os.makedirs("artifacts", exist_ok=True)

            # Save Raw Data
            df.to_csv(
                self.ingestion_config.raw_data_path,
                index=False,
                header=True
            )

            logger.info("Raw dataset saved successfully")

            # Train Test Split
            logger.info("Performing Train-Test Split")

            train_set, test_set = train_test_split(
                df,
                test_size=0.2,
                random_state=42
            )

            logger.info(
                "Train Shape: %s | Test Shape: %s",
                train_set.shape,
                test_set.shape,
            )

            # Save Train Data
            train_set.to_csv(
                self.ingestion_config.train_data_path,
                index=False,
                header=True
            )

            # Save Test Data
            test_set.to_csv(
                self.ingestion_config.test_data_path,
                index=False,
                header=True
            )

            logger.info("Train and Test files saved successfully")

            logger.info("Data Ingestion Completed Successfully")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            logger.error("Error occurred during data ingestion")
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion(r"notebook\data\stud.csv")

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
   
    print("The best working model r2-score value is: ",modeltrainer.initiate_model_trainer(train_arr,test_arr))