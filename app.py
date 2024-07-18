from flask import Flask, render_template, request
import os
import joblib
from pathlib import Path
import numpy as np
from src.StarbucksProject.pipeline.prediction import PredictionPipeline


app = Flask(__name__)  # initialize a flask app


@app.route('/', methods=['GET'])  # home page
def homePage():
    return render_template("index.html")


@app.route('/train', methods=['GET'])  # train the model
def training():
    os.system("python main.py")
    return "Model training successful"


@app.route('/predict', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':

        try:

            total_pop = int(request.form['total_pop'])
            males_per_100_females = float(request.form['males_per_100_females'])
            median_age = float(request.form['median_age'])
            median_rent = int(request.form['median_rent'])
            total_employed = int(request.form['total_employed'])
            per_capita_income = int(request.form['per_capita_income'])
            avg_household_size = float(request.form['avg_household_size'])
            enrolled_in_college = int(request.form['enrolled_in_college'])
            total_bachelors_degree = int(request.form['total_bachelors_degree'])
            total_same_residence = int(request.form['total_same_residence'])

            data = [total_pop, males_per_100_females, median_age, median_rent, total_employed, per_capita_income,
                    avg_household_size, enrolled_in_college, total_bachelors_degree, total_same_residence]

            data = np.array(data).reshape(1, 10)

            pred_pipe = PredictionPipeline(joblib.load(Path('final_model.joblib')))
            prediction = pred_pipe.predict(data)

            # obj = PredictionPipeline()
            # predict = obj.predict(data)

            # return render_template('results.html', prediction=str(predict))
            return render_template('results.html', prediction=f"{round(prediction[0], 2)} / 5")

        except Exception as e:
            print("Error - couldn't generate prediction", e)

    else:
        return render_template('index.html')


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8080)