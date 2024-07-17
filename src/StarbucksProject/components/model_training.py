import pandas as pd
import os
from src.StarbucksProject.entity.config_entity import ModelTrainerConfig
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.preprocessing import StandardScaler
import joblib


class ModelTrainer:

    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):

        X_train = pd.read_csv(self.config.x_train_path)
        y_train = pd.read_csv(self.config.y_train_path)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)

        abr = AdaBoostRegressor()
        abr.fit(X_train_scaled, y_train.values.ravel())

        joblib.dump(abr, os.path.join(self.config.root_dir, self.config.model_name))

