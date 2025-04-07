# This File is used to Connect to Constant File which contains the variables

from src.constants import *
from src.logger import logger
import os, sys

ROOT_DIR = ROOT_DIR

DATASET_URL = os.path.join(ROOT_DIR, DATA_DIR_KEY, DATA_NAME)
RAW_DATA_PATH = os.path.join(
    ROOT_DIR,
    ARTIFACT_DIR_KEY,
    TIMESTAMP,
    DATA_INGESTION_RAW_DIR_KEY,
)
TRAIN_DATA_PATH = os.path.join(
    ROOT_DIR,
    ARTIFACT_DIR_KEY,
    TIMESTAMP,
    DATA_INGESTION_DIR_KEY,
    DATA_INGESTION_INGESTED_TRAIN_DIR_KEY,
)
TEST_DATA_PATH = os.path.join(
    ROOT_DIR,
    ARTIFACT_DIR_KEY,
    TIMESTAMP,
    DATA_INGESTION_DIR_KEY,
    DATA_INGESTION_INGESTED_TEST_DIR_KEY,
)

# * New Variales Created for Data Transformation


class DataTransformationConfig:
    """Class Containing All the Data Transformation Pipeline Configuration"""

    def __init__(self):
        self.PRE_DATA_TRANSFORMATION_PATH = os.path.join(
            ROOT_DIR, ARTIFACT_DIR_KEY, PRE_DATA_TRANSFORMATION_DIR, TIMESTAMP, DATA_PROCESSED_DIR
        )

        self.FINAL_TRANSFORMATION_PATH_TRAIN = os.path.join(
            ROOT_DIR, ARTIFACT_DIR_KEY, DATA_TRANSFORM_DIR, TIMESTAMP, TRANSFORMED_DATA_TRAIN_DIR
        )
        self.FINAL_TRANSFORMATION_PATH_TEST = os.path.join(
            ROOT_DIR, ARTIFACT_DIR_KEY, DATA_TRANSFORM_DIR, TIMESTAMP, TRANSFORMED_DATA_TEST_DIR
        )
