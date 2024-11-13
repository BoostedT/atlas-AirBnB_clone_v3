#!/usr/bin/python3
"""Flask app that performs actions on the states table in hbtn_0e_0_usa"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Closes the current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
