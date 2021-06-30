# Dependencies required for the car_price
from flask import Blueprint, request, jsonify
import logging
import numpy as np
import pandas as pd
import json
import joblib
import pickle
from azureml.core.model import Model
from azureml.train.automl.runtime.automl_explain_utilities import automl_setup_model_explanations

# Create blueprint
car_price_bp = Blueprint('price', __name__, url_prefix='/api/v1/car_price')

# Called when the service is initially loaded
@car_price_bp.before_app_first_request
def load_models():
    global PRICE_MODEL_PATH, PRICE_EXPLAINER_PATH, GLOBAL_PRICE_RAW_FI_PATH, GLOBAL_PRICE_ENG_FI_PATH
    PRICE_PATH = 'car_dealership/price/static'
    PRICE_MODEL_PATH           = f'{PRICE_PATH}/model.sav'
    PRICE_EXPLAINER_PATH       = f'{PRICE_PATH}/scoring_explainer.pkl'
    GLOBAL_PRICE_RAW_FI_PATH   = f'{PRICE_PATH}/global_raw_feature_importance.json'
    GLOBAL_PRICE_ENG_FI_PATH   = f'{PRICE_PATH}/global_engineered_feature_importance.json'
    global PRICE_MODEL, PRICE_EXPLAINER, GLOBAL_PRICE_RAW_FI, GLOBAL_PRICE_ENG_FI
    # Load the registered model file
    with open(PRICE_MODEL_PATH, 'rb') as f:
        PRICE_MODEL = joblib.load(f)
    logging.debug(f'PRICE_MODEL = {PRICE_MODEL}')
    # Load the scoring explainer file
    with open(PRICE_EXPLAINER_PATH, 'rb') as f:
        PRICE_EXPLAINER = joblib.load(f)
    logging.debug(f'PRICE_EXPLAINER = {PRICE_EXPLAINER}')
    # Load the local engineered feature importance
    with open(GLOBAL_PRICE_RAW_FI_PATH) as f:
        GLOBAL_PRICE_RAW_FI = json.load(f)
    logging.debug(f'GLOBAL_PRICE_RAW_FI = {GLOBAL_PRICE_RAW_FI}')
    # Load the global engineered feature importance
    with open(GLOBAL_PRICE_ENG_FI_PATH) as f:
        GLOBAL_PRICE_ENG_FI = json.load(f)
    logging.debug(f'GLOBAL_PRICE_ENG_FI = {GLOBAL_PRICE_ENG_FI}')

@car_price_bp.route('/prediction', methods=('POST', ))
def predict_price():
    car_price_input = request.json
    logging.debug(f'car_price_input = {car_price_input}')
    logging.debug(f'type(car_price_input) = {type(car_price_input)}')
    # Convert json to dataframe
    # car_price_input = pd.read_json(car_price_input, orient='records')
    car_price_input = pd.DataFrame(car_price_input)
    # Perform prediction
    predictions = PRICE_MODEL.predict(car_price_input)
    # Setup for inferencing explanations
    explainer_setup = automl_setup_model_explanations(PRICE_MODEL, 
                                                      X_test=car_price_input,  
                                                      task='regression')
    # Retrieve model explanations for engineered explanations
    engineered_local_feature_importance = PRICE_EXPLAINER.explain(explainer_setup.X_test_transform, 
                                                                  get_raw=False)
    # Retrieve model explanations for raw explanations
    raw_local_feature_importance = PRICE_EXPLAINER.explain(explainer_setup.X_test_transform, 
                                                           get_raw=True)
    
    # Serialize to json
    return jsonify({
        'predictions': predictions.tolist(), 
        'raw_feature_names': explainer_setup.raw_feature_names,
        'engineered_feature_names': explainer_setup.engineered_feature_names,
        'raw_local_feature_importance': raw_local_feature_importance, 
        'engineered_local_feature_importance': engineered_local_feature_importance,
    })

@car_price_bp.route('/global_feature_importance', methods=('GET', ))
def get_price_feature_importances():
    return jsonify([GLOBAL_PRICE_RAW_FI, GLOBAL_PRICE_ENG_FI])