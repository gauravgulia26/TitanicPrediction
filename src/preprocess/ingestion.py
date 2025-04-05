from src.logger import logger
from src.exceptions import CustomException
from src.YAML import LoadYaml
from pathlib import Path
import pandas as pd
import numpy as np

file_name = "./config.yaml"

yaml_path = str(Path(file_name).resolve())


try:
    yaml_file = LoadYaml(url=yaml_path).Load_Yaml()
except Exception as e:
    err = CustomException(error_message=e)
    err.log_exception()
else:
    data_path = yaml_file['data']['data_url']
    logger.info(f"Path Loaded {data_path}")

class LoadData:
    def __init__(self,url:str = data_path):
        self.url = url
        pass

    def LoadFile(self):
        try:
            df = pd.read_csv(f'{self.url}?raw=true')
        except Exception as e:
            err = CustomException(error_message=e)
            err.log_exception()
        else:
            logger.info("Dataframe Successfully Loaded")
            return df



