import pandas as pd
import os
from src.StarbucksProject.entity.config_entity import ModelTrainerConfig
from sklearn.neighbors import KNeighborsRegressor
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

        knr = KNeighborsRegressor()
        knr.fit(X_train_scaled, y_train)

        joblib.dump(knr, os.path.join(self.config.root_dir, self.config.model_name))