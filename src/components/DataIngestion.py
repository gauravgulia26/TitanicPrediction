from src.constants import *
from src.config.configuration import *
from src.logger import logger
from src.exceptions import CustomException
import os, sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from pydantic import BaseModel, Field


class DataIngestionConfig(BaseModel):
    """Class Containing all the Configuration for Data Ingestion

    Args:
        BaseModel (__type__): Inherited from Pydantic Base Model Class
    """

    raw_data_path: str = RAW_DATA_PATH
    """Original Path of the Data
    """
    train_data_path: str = TRAIN_DATA_PATH
    """Path to Store Training Data After Splitting
    """
    test_data_path: str = TEST_DATA_PATH
    """Path to store the Testing Data After Splitting
    """


class DataIngestion(BaseModel):
    """Main Class to Execute Data Ingestion Pipeline.

    Args:
        BaseModel (_type_): Pydantic Base Model Class
    """

    data_ingestion_config: DataIngestionConfig = Field(
        description="Must be refered to the class containing Data Ingestion Config",
        default_factory=DataIngestionConfig,
    )

    def __InitiateIngestion(self):
        try:
            df = pd.read_csv(DATASET_URL)
            logger.info(f"Dataset Loaded Successfully from {DATASET_URL}")
            os.makedirs(self.data_ingestion_config.raw_data_path, exist_ok=True)
            logger.info(
                f"Raw Data Folder Successfully Created at {self.data_ingestion_config.raw_data_path}"
            )
            df.to_csv(
                os.path.join(
                    self.data_ingestion_config.raw_data_path, DATA_INGESTION_RAW_FILE_NAME
                )
            )
            logger.info(f"Fetched Data Successfully Saved to {RAW_DATA_PATH}")
        except FileNotFoundError as e:
            err = CustomException(error_message=e)
            err.log_exception()
        except AttributeError as e:
            err = CustomException(error_message=e)
            err.log_exception()
        except Exception as e:
            err = CustomException(error_message=e)
            err.log_exception()

        return df

    def InitiateIngestion(self):
        try:
            df = self.__InitiateIngestion()
            X = df.drop(columns="Survived", axis=1)
            y = df["Survived"]
            logger.debug(
                "Successfully Splitted into X,Y\n Procedding to Split into Training and Testing Set"
            )
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.33, random_state=42
            )
            logger.info("Successfully Splitted into Training and Testing Set")

        except Exception as e:
            err = CustomException(error_message=e)
            err.log_exception()
        else:
            try:
                os.makedirs(self.data_ingestion_config.train_data_path, exist_ok=True)
                os.makedirs(self.data_ingestion_config.test_data_path, exist_ok=True)
                logger.info("Successfully Created the Testing and Training Directory")
                pd.concat((X_train,y_train),axis=1).to_csv(
                    os.path.join(
                        self.data_ingestion_config.train_data_path,
                        DATA_INGESTION_INGESTED_TRAIN_FILE_NAME,
                    )
                )
                pd.concat((X_test,y_test),axis=1).to_csv(
                    os.path.join(
                        self.data_ingestion_config.test_data_path,
                        DATA_INGESTION_INGESTED_TEST_FILE_NAME,
                    )
                )
                logger.info(
                    f"Training Data Sucessfully Saved at {self.data_ingestion_config.train_data_path}"
                )
                logger.info(
                    f"Testing Data Sucessfully Saved at {self.data_ingestion_config.test_data_path}"
                )
            except Exception as e:
                err = CustomException(error_message=e)
                err.log_exception()


if __name__ == "__main__":
    try:
        obj = DataIngestion()
    except Exception as e:
        err = CustomException(error_message=e)
        err.log_exception()
    else:
        obj.InitiateIngestion()
