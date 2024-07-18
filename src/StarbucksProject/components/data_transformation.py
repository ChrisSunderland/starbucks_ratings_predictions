from src.StarbucksProject import logger
from sklearn.model_selection import train_test_split
import pandas as pd
import os
from src.StarbucksProject.entity.config_entity import DataTransformationConfig


class DataTransformation:

    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def split_data(self):

        data = pd.read_csv(self.config.data_path)
   
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

        logger.info("split data into training and rest sets")
        X_train.to_csv(os.path.join(self.config.root_dir, "X_train.csv"), index=False)
        X_test.to_csv(os.path.join(self.config.root_dir, "X_test.csv"), index=False)
        y_train.to_csv(os.path.join(self.config.root_dir, "y_train.csv"), index=False)
        y_test.to_csv(os.path.join(self.config.root_dir, "y_test.csv"), index=False)

