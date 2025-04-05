from src.logger import logger
from src.exceptions import CustomException
from pydantic import BaseModel, Field
from typing import List
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer


class MakePipeline(BaseModel):
    num_col: List = Field(title="List of all the Non Null Numerical Columns")
    cat_col: List = Field(title="List of all the Non Null Categorical Columns")

    def Transform(self):
        """This Function will give you a final Column Transformer Ready to be Used.
        """

        NumPipe, CatPipe = self.CreatePipe()
        imputer_trf = ColumnTransformer(
            transformers=[
                ("Numerical Pipeline", NumPipe, self.num_col),
                ("Categorical Pipeline", CatPipe, self.cat_col),
            ],
            remainder="passthrough",
        )

        imputer_trf.set_output(transform='pandas')

        return imputer_trf

    def CreatePipe(self):
        Num_Si = SimpleImputer(strategy="median")
        Cat_Si = SimpleImputer(strategy="most_frequent")

        NumericalPipeline = Pipeline(steps=[("Numerical SimpleImputer", Num_Si)])

        CategoricalPipeline = Pipeline(steps=[("Categorical Imputer", Cat_Si)])

        return NumericalPipeline, CategoricalPipeline
