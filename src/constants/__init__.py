# This file is used to define the project wide variables for reuse.

import sys,os
from datetime import datetime


def get_current_time_stamp():
    return f'{datetime.now().strftime('%d:%m:%Y-%H:%M:%S')}'

TIMESTAMP = get_current_time_stamp()

#* This will fetch the data from specified path and then Proceed With Data Ingestion Step

ROOT_DIR = os.getcwd()
DATA_NAME = 'output.csv'
DATA_DIR_KEY = 'data/raw'

# Next step is to save the data into artifact folder

#* Folder Structure: 
# ----------------------------------------------------------------------

# * Artifact Folder is used to store the data after fetching the data from remote/local and save to respecting directories.
# *Artifact/DataIngestion/RawData/raw.csv

# *Artifact/DataIngestion/IngestedData/train/train.csv
# *Artifact/DataIngestion/IngestedData/test/test.csv

# ----------------------------------------------------------------------

# * Data Ingestion -> The steps are to download the data and then split it into 
# * Training and Testing Set

# ----------------------------------------------------------------------

# * Creating Directory Names:

ARTIFACT_DIR_KEY = 'Artifact'
DATA_INGESTION_DIR_KEY = 'DataIngestion'
DATA_INGESTION_RAW_DIR_KEY = 'RawData'
DATA_INGESTION_INGESTED_DIR_KEY = 'IngestedData'
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY = 'Train'
DATA_INGESTION_INGESTED_TEST_DIR_KEY = 'Test'

# * Creating File Names:

DATA_INGESTION_RAW_FILE_NAME = 'raw.csv'
DATA_INGESTION_INGESTED_TRAIN_FILE_NAME = 'train.csv'
DATA_INGESTION_INGESTED_TEST_FILE_NAME = 'test.csv'

# ---------------------------------------------------







