from ingestion import LoadData
from src.exceptions import CustomException
from src.logger import logger
from src.decorators import ValidateDf
from src.pipeline import MakePipeline
from CheckNa import FindNa
from CheckNormality import CheckNormality
from YeoJohn import YeoJohn
from scipy.stats import shapiro
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from typing import List
import pandas as pd
import numpy as np
import json
import os


class PreprocessData:
    def __init__(self):
        pass

    def LoadPreprocessor(self):
        try:
            data = LoadData().LoadFile()
        except Exception as e:
            err = CustomException(error_message=e)
            err.CreateException()

        num = data.select_dtypes(exclude=["object", "bool", "category"])
        cat = data.select_dtypes(include=["object", "bool", "category"])
        data_name = 'output.csv'
        data_dir = 'data/raw'
        data_path = os.path.join(os.getcwd(),data_dir,data_name)
        data.to_csv(data_path)
        logger.info(f'Data Saved to {data_dir} as {data_name}')

        return data, num, cat

    def StartNumPreprocessing(self):
        df, num, _ = self.LoadPreprocessor()
        logger.info(f"Average NA Values:\n{df.isna().mean()}")
        logger.info(f"Duplicate Values:\n{df.duplicated().sum()}")

        try:
            NaObject = FindNa(x=df)
        except Exception as e:
            err = CustomException(e)
            err.log_exception()
        else:
            full_na, num, cat = NaObject.Start()

        try:
            PipeObject = MakePipeline(num_col=num, cat_col=cat)
        except Exception as e:
            err = CustomException(error_message=e)
            err.log_exception()

        logger.info("Pipeline Fetched Successfully, Applying Transformation !!")
        transformation = PipeObject.Transform()

        try:
            data = transformation.fit_transform(df)
            labels = transformation.get_feature_names_out()
        except Exception as e:
            err = CustomException(error_message=e)
            err.log_exception()

        final_df = pd.DataFrame(data=data, columns=labels)
        logger.info(f"Final Null Values after Processing\n{final_df.isnull().sum()}")

        cleaned_num = final_df.select_dtypes(exclude=["category", "bool", "object"])
        skewness = {}
        for _ in cleaned_num:
            skewness[_] = cleaned_num[_].skew()

        try:
            NormalObject = CheckNormality(x=cleaned_num)
        except ValueError as e:
            err = CustomException(error_message=e)
            err.log_exception()

        normal_col, not_normal_col = NormalObject.Start()
        try:
            powertrf_object = YeoJohn(x=cleaned_num)
        except ValueError as e:
            err = CustomException(error_message=e)
            err.log_exception()

        powertrf = powertrf_object.ApplyYeo()

        for _ in not_normal_col:
            try:
                final_df[_] = powertrf.fit_transform(final_df[_].values.reshape(-1, 1))
            except Exception as e:
                err = CustomException(e)
                err.log_exception()
        logger.info("All Non Normal Columns have Been tranformed to Normal Distribution")
        new_skewness = {

        }

        for _ in cleaned_num:
            new_skewness[_] = final_df[_].skew()

        logger.info("Below is the Comparison before and after skewness")
        logger.info('-----------------------------------------')
        logger.info("Before")
        logger.info('-----------------------------------------')
        logger.info(f"{json.dumps(skewness,indent=4)}")
        logger.info('-----------------------------------------')
        logger.info("After")
        logger.info(f"{json.dumps(new_skewness,indent=4)}")
        logger.info('-----------------------------------------')



if __name__ == "__main__":

    obj = PreprocessData()
    obj.StartNumPreprocessing()
