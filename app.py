
from flask import Flask, render_template, request
import pandas as pd
import pickle
import os


app = Flask(__name__)


# ---------------------------------------------------
# Load Model and Preprocessor
# ---------------------------------------------------

model_path = os.path.join("artifacts", "model.pkl")
proprocessor_path = os.path.join("artifacts", "proprocessor.pkl")


with open(model_path, "rb") as file:
    model = pickle.load(file)


with open(proprocessor_path, "rb") as file:
    preprocessor = pickle.load(file)


# ---------------------------------------------------
# Home Route
# ---------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def predict():

    prediction = None

    if request.method == "POST":

        # Get data from form
        gender = request.form["gender"]
        race_ethnicity = request.form["race_ethnicity"]
        parental_level_of_education = request.form[
            "parental_level_of_education"
        ]
        lunch = request.form["lunch"]
        test_preparation_course = request.form[
            "test_preparation_course"
        ]

        reading_score = float(request.form["reading_score"])
        writing_score = float(request.form["writing_score"])


        # Create DataFrame
        input_data = pd.DataFrame({
            "gender": [gender],
            "race_ethnicity": [race_ethnicity],
            "parental_level_of_education": [
                parental_level_of_education
            ],
            "lunch": [lunch],
            "test_preparation_course": [
                test_preparation_course
            ],
            "reading_score": [reading_score],
            "writing_score": [writing_score]
        })


        # Apply preprocessing
        input_data = preprocessor.transform(input_data)


        # Make prediction
        prediction = model.predict(input_data)[0]


        # Round prediction
        prediction = round(float(prediction), 2)


    return render_template(
        "index.html",
        prediction=prediction
    )


# ---------------------------------------------------
# Run Application
# ---------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)

