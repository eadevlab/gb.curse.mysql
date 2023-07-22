import pandas as pd
import os
from joblib import load
from app.run import get_model
pd.options.mode.chained_assignment = None

json_data = [
    {
        "age": 30,
        "job": "unemployed",
        "marital":"married",
        "education":"primary",
        "default": "no",
        "balance":1787,
        "housing": "no",
        "loan":"no",
        "contact":"cellular",
        "day":19,
        "month":"oct",
        "duration":79,
        "campaign":1,
        "pdays":-1,
        "previous":0,
        "poutcome":"unknown"
    },
    {
        "age": 30,
        "job": "unemployed",
        "marital":"married",
        "education":"primary",
        "default": "no",
        "balance":1787,
        "housing": "no",
        "loan":"no",
        "contact":"cellular",
        "day":19,
        "month":"oct",
        "duration":79,
        "campaign":1,
        "pdays":-1,
        "previous":0,
        "poutcome":"unknown"
    },
    {
        "age": 30,
        "job": "unemployed",
        "marital":"married",
        "education":"primary",
        "default": "no",
        "balance":1787,
        "housing": "no",
        "loan":"no",
        "contact":"cellular",
        "day":19,
        "month":"oct",
        "duration":79,
        "campaign":1,
        "pdays":-1,
        "previous":0,
        "poutcome":"unknown"
    }
]


input_data = pd.DataFrame(json_data)

APP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')

model_path = os.path.join(APP_PATH,'models/bank_model.joblib')
model = get_model(model_path)

predictions = model.predict(input_data)

assert predictions[0] == 0