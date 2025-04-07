import numpy as np
import pandas as pd
import os, sys
import joblib

from src.logger import logger
from src.exceptions import CustomException
from src.config.configuration import DATASET_URL, DataTransformationConfig
from pydantic import BaseModel, Field
from typing import Type, List

# from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from rich import print


class _FeatureEnginerring(BaseModel, arbitrary_types_allowed=True):
    url: str = Field(description="Path of the Data", default=str(DATASET_URL))

    def InitiateFeatureEnginerring(self):
        df = pd.read_csv(self.url)
        logger.info(f"Dropping Columns")
        df.drop(columns=["Unnamed: 0", "Name"], axis=1, inplace=True)
        logger.info("Making New Features")
        df["CabinNumber"] = df["Cabin"].str.extract(r"([a-zA-Z]+)")
        df["RoomNumber"] = df["Cabin"].str.extract(r"([0-9]+)")
        logger.info("Dropping Columns")
        df.drop(columns=["Cabin", "Ticket", "PassengerId"], inplace=True)
        logger.info("Feature Enginerring Completed, Procedding to creating pipeline")
        return df


class _CreatePipeline(BaseModel, arbitrary_types_allowed=True):
    x: pd.DataFrame = Field(description="Feature Enginerred Dataframe to Create Pipeline")

    def InitiatePipeline(self):
        """Creates ordinal, numerical and Categorical Pipleine

        Returns:
            tuple: Return tuple of numerical,categorical,ordinal Sklearn.pipeline object and Numerical,Categorical, Ordinal Column List
        """
        df = self.x
        num_col = df.select_dtypes(exclude=["object", "category", "bool"]).columns.tolist()
        cat_col = (
            df.select_dtypes(include=["object", "category", "bool"])
            .drop(columns="Sex")
            .columns.tolist()
        )
        ordinal_col = ["Sex"]
        ordinal_categories = [df["Sex"].unique().tolist()]

        numerical_pipeline = Pipeline(
            steps=[("Numerical Imputing", SimpleImputer(strategy="median"))]
        )

        categorical_pipeline = Pipeline(
            steps=[
                ("Categorical Imputing", SimpleImputer(strategy="most_frequent")),
                (
                    "Categorical Encoding",
                    OneHotEncoder(drop="first", sparse_output=False),
                ),
            ]
        )

        ordinal_pipeline = Pipeline(
            steps=[
                ("Ordinal Imputing", SimpleImputer(strategy="most_frequent")),
                (
                    "Ordinal Encoding",
                    OrdinalEncoder(categories=ordinal_categories),
                ),
            ]
        )
        logger.info("Pipeline Created, Procedding for Transformation")
        return (
            numerical_pipeline,
            categorical_pipeline,
            ordinal_pipeline,
            num_col,
            cat_col,
            ordinal_col,
        )


class ApplyTransformation:
    def __init__(self):
        pass

    def Transform(self):
        obj = _FeatureEnginerring()
        df = obj.InitiateFeatureEnginerring()
        obj2 = _CreatePipeline(x=df)
        num_pipe, cat_pipe, ord_pipe, num_col, cat_col, ordinal_col = obj2.InitiatePipeline()
        transformation = ColumnTransformer(
            transformers=[
                ("Numerical Pipeline", num_pipe, num_col),
                (
                    "Categorical Pipeline",
                    cat_pipe,
                    cat_col,
                ),
                ("Ordinal Pipleine", ord_pipe, ordinal_col),
            ],
            remainder="passthrough",
        )
        logger.info("Transformation Created !!")
        logger.debug("Applying Transformation !!")
        logger.info("Saving the Preprocessor into Pickle File")

        try:
            config_obj = DataTransformationConfig()
        except Exception as e:
            err = CustomException(error_message=e)
            err.log_exception()

        processor_path = config_obj.PRE_DATA_TRANSFORMATION_PATH

        file_name = "preprocess.pkl"

        full_path = os.path.join(str(processor_path), file_name)

        try:
            os.makedirs(processor_path,exist_ok=True)
            joblib.dump(filename=full_path,value=transformation)
        except Exception as e:
            err = CustomException(error_message=e)
            err.log_exception()
        else:
            logger.info(f"Preprocessor Successfully Saved to {full_path}")

        transformed_data = transformation.fit_transform(df)

        data = transformed_data
        labels = transformation.get_feature_names_out()

        final_data = pd.DataFrame(data=data, columns=labels)

        return final_data


if __name__ == "__main__":
    try:
        obj = ApplyTransformation()
        trf = obj.Transform()
    except Exception as e:
        err = CustomException(error_message=e)
        err.log_exception()
    else:
        if sum(trf.isna().sum()) == 0:
            logger.debug(
                "There are no null values present in the data !! Transformation Completed"
            )
        else:
            raise ValueError("NA Values Still Present !!")
