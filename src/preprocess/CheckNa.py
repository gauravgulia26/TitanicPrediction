from src.logger import logger
from pydantic import BaseModel, Field
import pandas as pd


class FindNa(BaseModel):
    x: pd.DataFrame = Field(
        title="Numerical Dataframe",
        description="Dataframe containing only numerical values of Data Frame.",
    )

    def Start(self):
        """This Method will return Numerical and Categorical Part of Main df\n
        along with the NA Dataframe!!

        Returns:
            _type_: _description_
        """
        df = self.x
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

        return null_col, num, cat

    class Config:
        arbitrary_types_allowed = True
