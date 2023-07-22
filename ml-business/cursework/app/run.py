import pandas as pd
import os

import flask

from flask_cors import CORS, cross_origin
from joblib import load

from conf.dicts import CATEGORICAL_FEATURES_MAPS
from conf.pipes import ColumnSelector, CategoryTransform

# initialize our Flask application and the model
app = flask.Flask(__name__)
CORS(app)

APP_PATH = os.path.dirname(os.path.abspath(__file__))


def get_model(model_path):
	model = None
	with open(model_path, 'rb') as f:
		model = load(f)
	return model

model_path = os.environ.get('MODELS_PATH', os.path.join(APP_PATH,'models/bank_model.joblib'))
model = get_model(model_path)

@app.route("/", methods=["GET"])
def index():
	pass

@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():

	data = {"success": False}

	request_json = flask.request.get_json()

	try:
		data['predictions'] = model.predict(
			pd.DataFrame(request_json)
		)
	except AttributeError as e:
		data['success'] = False
		return flask.jsonify(data)


	data["success"] = True
	return flask.jsonify(data)


if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 8080))
	app.run(host='0.0.0.0', debug=True, port=port)