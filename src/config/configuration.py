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