import joblib
from pathlib import Path


class PredictionPipeline:

    def __init__(self, model):  # maybe pass in the model

         # self.model = joblib.load(Path('final_model/tuned_model.joblib'))
        self.model = model

    def predict(self, data):

        prediction = self.model.predict(data)

        return prediction
