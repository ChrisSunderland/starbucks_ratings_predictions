import os
from pathlib import Path
from src.StarbucksProject.entity.config_entity import ModelEvaluationConfig
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
from src.StarbucksProject.utils.common import save_json


class ModelEvaluation:

    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def get_mae(self, actual, pred):

        mae = mean_absolute_error(actual, pred)
        return mae

    def tune_with_mlflow(self):

        model = joblib.load(self.config.model_path)

        X_train = pd.read_csv(self.config.x_train_path)
        y_train = pd.read_csv(self.config.y_train_path)
        X_test = pd.read_csv(self.config.x_test_path)
        y_test = pd.read_csv(self.config.y_test_path)

        pipe = Pipeline([('scaler', StandardScaler()),
                         ('abr', model)])

        param_grid = {"abr__" + k: list(v) for k, v in dict(self.config.all_params).items()}

        gs = GridSearchCV(estimator=pipe,
                          param_grid=param_grid,
                          cv=3,
                          scoring='neg_mean_absolute_error',
                          verbose=1,
                          n_jobs=-1)

        gs.fit(X_train, y_train.values.ravel())
        tuned_model = gs.best_estimator_
        joblib.dump(tuned_model, os.path.join(self.config.root_dir, self.config.tuned_model))

        # ML FLOW
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():

            predicted_vals = tuned_model.predict(X_test)
            test_mae = self.get_mae(y_test, predicted_vals)

            scores = {"mae": test_mae}
            save_json(path=Path(self.config.metric_file_name), data=scores)  # save metrics locally

            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("mae", test_mae)

            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(model, "model", registered_model_name="AdaBoost Tuned")
            else:
                mlflow.sklearn.log_model(model, "model")

        return tuned_model
