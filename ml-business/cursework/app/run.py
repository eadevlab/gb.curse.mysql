from keras.models import load_model
import pandas as pd
import os

import flask

from time import strftime
from flask_cors import CORS, cross_origin

# initialize our Flask application and the model
app = flask.Flask(__name__)
CORS(app)

def get_model(model_path):
	model = None
	with open(model_path, 'rb') as f:
		model = load_model(f)
	return model

modelpath = os.environ.get('MODELS_PATH', "/app/models/model.h5")
model = get_model(modelpath)

@app.route("/", methods=["GET"])
def index():
	pass

@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():

	data = {"success": False}
	dt = strftime("[%Y-%b-%d]")

	request_json = flask.request.get_json()

	try:
		pass
	except AttributeError as e:
		data['success'] = False
		return flask.jsonify(data)


	data["success"] = True
	return flask.jsonify(data)


if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 8180))
	app.run(host='0.0.0.0', debug=True, port=port)