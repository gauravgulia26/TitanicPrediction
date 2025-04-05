from src.logger import logger
from pydantic import BaseModel, Field, field_validator
from src.YAML import LoadYaml
from src.exceptions import CustomException
import pandas as pd
from scipy.stats import shapiro

try:
    yaml_file = LoadYaml().Load_Yaml()
except FileNotFoundError as e:
    err = CustomException(e)
    err.log_exception()
except Exception as e:
    err = CustomException(e)
    err.log_exception()


class CheckNormality(BaseModel):
    x: pd.DataFrame = Field(title="Non NA Numerical Df")

    @field_validator("x")
    def Check_For_Na(cls, value: pd.DataFrame):
        if not sum(value.isnull().sum().values) == 0:
            raise ValueError(
                f"Your Dataframe Contains Null Values, Please Impute before Proceeding !"
            )
        return value

    def Start(self):
        num = self.x
        logger.info(f"Checking for Normality using Shapiro-Wilk Test")
        normal_col = []
        not_normal_col = []
        for column in num:
            data = num[column]
            if len(data) >= 3:
                stat, p_value = shapiro(data)
                if p_value > 0.05:
                    logger.info(f"  {column} appears to be normally distributed.\n")
                    normal_col.append(column)
                else:
                    logger.info(f"  {column} does not appear to be normally distributed.\n")
                    not_normal_col.append(column)
            else:
                raise ValueError(
                    f"Column '{column}' does not have enough data points for the Shapiro-Wilk test.\n"
                )
        if len(not_normal_col) < num.shape[1]:
            logger.info(f"Non Normally Distributed Columns are {not_normal_col}")
            logger.info(f"Normally Distributed Columns are {normal_col}")
        return normal_col, not_normal_col

    class Config:
        arbitrary_types_allowed = yaml_file['pydantic']["arbitrary_types_allowed"]
