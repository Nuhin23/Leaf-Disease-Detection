from flask import Blueprint

prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.route("/predict")
def predict():
    return "Prediction Page"
