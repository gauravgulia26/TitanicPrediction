import logging, coloredlogs
import os
from pathlib import Path
from src.YAML import LoadYaml


logger = logging.getLogger(__name__)
coloredlogs.install(
    level="DEBUG",
    logger=logger,
)

