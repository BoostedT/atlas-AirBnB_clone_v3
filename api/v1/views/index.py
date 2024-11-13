#!/usr/bin/python3
"""Index view for API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each objects by type"""
    stats = {
        "users": storage.count("User"),
        "states": storage.count("State"),
        "cities": storage.count("City"),
    }
    return jsonify(stats)
