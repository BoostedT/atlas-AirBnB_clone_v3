#!/usr/bin/python3
"""Flask app that performs actions on the states table in hbtn_0e_0_usa"""

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
from api.v1.views import app_views
from models import storage


app = Flask(__name__)


app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host="host", port=port, threaded=True)
