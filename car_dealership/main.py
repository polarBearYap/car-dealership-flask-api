# Dependencies required for the car_price
from flask import Blueprint, request, jsonify, url_for
import logging
import numpy as np
import pandas as pd
import json
import joblib
import pickle
from azureml.core.model import Model
from azureml.train.automl.runtime.automl_explain_utilities import automl_setup_model_explanations
from car_dealership import app

@app.route('/')
def index():
	return 'Successful!'

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route("/site_map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if ("POST" in rule.methods or "GET" in rule.methods) and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return jsonify(links)