from sklearn.preprocessing import PowerTransformer
from src.logger import logger
from src.exceptions import CustomException
from pydantic import BaseModel, Field, field_validator
import pandas as pd

trf = PowerTransformer(standardize=False)

class YeoJohn(BaseModel,arbitrary_types_allowed=True):
    x: pd.DataFrame = Field(title="Numerical Dataframe from Main DF (Non Null)")

    @field_validator('x')
    def ValidateNull(cls,value:pd.DataFrame):
        total = sum(value.isnull().sum())
        if not total == 0:
            raise ValueError('Your DataFrame contains Null Value, Proceed With Imputing First')
        return value
    

    def ApplyYeo(self):
        """This Function will Return Yeo Johnson Transformation With Standardize being False"""
        return trf

