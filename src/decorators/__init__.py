import pandas as pd
from src.exceptions import CustomException
import functools
import pandas as pd

def ValidateDf(func):
    """Decorator to validate that the first argument is a pandas DataFrame."""
    @functools.wraps(func)
    def wrapper(self, x, *args, **kwargs):
        if not isinstance(x, pd.DataFrame):
            raise CustomException(
                f"Only Pandas DataFrames are allowed, got {type(x).__name__} instead"
            )
        return func(self, x, *args, **kwargs)
    return wrapper

def ValidateNum(func):
    @functools.wraps(func)
    def wrapper(self,x:pd.DataFrame):
        num_col = x.select_dtypes(exclude=["object", "bool", "category"]).columns.tolist()
        total_col = x.columns.tolist()
        if not len(num_col) == len(total_col):
            raise ValueError("Please pass the subset of df containing all numerical columns only !!")
        return func(self,x)
    return wrapper
