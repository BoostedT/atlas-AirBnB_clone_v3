#!/usr/bin/python3
"""Index view for API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status"""
    return jsonify({"status": "OK"})
