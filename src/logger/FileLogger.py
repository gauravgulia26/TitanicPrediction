from pathlib import Path
from logger import logger
from src.YAML import LoadYaml

file_name = "./config.yaml"
file_path = str(Path(file_name).resolve())

try:
    yaml_file = LoadYaml(url=file_path)
except FileNotFoundError as e:
    logger.error(f"{e} Occured")
except Exception as e:
    logger.error(f"{e} Occured")
else:
    try:
        yaml_file = yaml_file.Load_Yaml()
    except FileNotFoundError as e:
        logger.error(f"{e}")
    except Exception as e:
        logger.error(f"{e}")
    else:
        logger.info("YAML File Loaded")

LOG_FILE_NAME = yaml_file['logger']['file_name']
LOG_FILE_PATH= yaml_file['logger']['file_name']


# This can be changed to make a logger that logs to file not to terminal when needed.