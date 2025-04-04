from src.ingestion import LoadData
from src.exceptions import CustomException
from src.logger import logger
from src.decorators import ValidateDf
from src.pipeline import MakePipeline
from scipy.stats import shapiro
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from typing import List
import pandas as pd


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

        return data, num, cat

    @ValidateDf
    def __GetNaValues(self, x: pd.DataFrame):
        df = x
        logger.info(f"Starting to Find the Columns Containing Null Values")
        null_col = df.columns[df.isnull().mean() > 0]
        num = df[null_col].select_dtypes(exclude=["object", "category", "bool"])
        cat = df[null_col].select_dtypes(include=["object", "category", "bool"])
        logger.info(f"Numerical Column {num.columns.tolist()} contains null values !!")
        logger.info(f"Categorical Column {cat.columns.tolist()} contains null values !!")
        logger.info("Checking if CCA can be applied or not")

        num_cols_with_missing = num.isna().mean()
        num_cols_low_missing = num_cols_with_missing[num_cols_with_missing < 0.05]

        if len(num_cols_low_missing) == 0:
            logger.info(
                "There are no numerical columns with less than 5% null values,\nCCA can't be applied, moving to Mean Median Mode Imputation"
            )
        else:
            target_col_2 = num_cols_low_missing.index.tolist()
            logger.info(
                f"{target_col_2} numerical columns contain less than 5% null values, CCA can be considered"
            )
        cat_cols_with_missing = cat.isna().mean()
        cat_cols_low_missing = cat_cols_with_missing[cat_cols_with_missing < 0.05]

        if len(cat_cols_low_missing) == 0:
            logger.info(
                "There are no categorical columns with less than 5% null values,\nCCA can't be applied, moving to Mean Median Mode Imputation"
            )
        else:
            target_col = cat_cols_low_missing.index.tolist()
            logger.info(
                f"{target_col} categorical columns contain less than 5% null values, CCA can be considered"
            )

        return num, cat

    @ValidateDf
    def __CheckNormality(self, x: pd.DataFrame):
        num = x
        logger.info(f"Checking for Normality using Shapiro-Wilk Test")
        normal_col = []
        not_normal_col = []
        for column in num:
            data = num[column].dropna()
            if len(data) >= 3:
                stat, p_value = shapiro(data)
                if p_value > 0.05:
                    logger.info(f"  {column} appears to be normally distributed.\n")
                    normal_col.append(column)
                else:
                    logger.info(f"  {column} does not appear to be normally distributed.\n")
                    not_normal_col.append(column)
            else:
                raise CustomException(
                    f"Column '{column}' does not have enough data points for the Shapiro-Wilk test.\n"
                ).CreateException()
        if len(not_normal_col) == num.shape[1]:
            logger.critical(f"All Columns are Skewed for this Data\n{not_normal_col}")
        if len(not_normal_col) < num.shape[1]:
            logger.info(f"Non Normally Distributed Columns are {not_normal_col}")
            logger.info(f"Normally Distributed Columns are {normal_col}")
        return normal_col, not_normal_col

    def StartNumPreprocessing(self):
        df, num, _ = self.LoadPreprocessor()
        logger.info(f"Average NA Values:\n{df.isna().mean()}")
        logger.info(f"Duplicate Values: \n{df.duplicated().sum()}")
        num, cat = self.__GetNaValues(df)
        try:
            PipeObject = MakePipeline(num_col=num,cat_col=cat)
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
        logger.info(f"Final Null Values after Processing\n {final_df.isnull().sum()}")
        logger.info("All Null Values has been handled, Next Step is to Check Normality")
        transformed_num = final_df.select_dtypes(exclude=['object','bool','category'])
        normal_col, not_normal_col = self.__CheckNormality(transformed_num)


if __name__ == "__main__":

    obj = PreprocessData()
    obj.StartNumPreprocessing()
