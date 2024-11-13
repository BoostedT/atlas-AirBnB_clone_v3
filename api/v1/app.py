#!/usr/bin/python3
"""Flask app that performs actions on the states table in hbtn_0e_0_usa"""

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
from os import getenv


app = Flask(__name__)


app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
