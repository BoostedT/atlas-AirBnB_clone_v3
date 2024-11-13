#!/usr/bin/python3
"""Blueprint for the API"""

from flask import Blueprint, jsonify, request, abort
from models import storage
from models.user import User

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User)
    user_list = []
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json(silent=True)()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(email=data['email'], password=data['password'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json(silent=True)()
    if data is None:
        abort(400, 'Not a JSON')
    ignored_fields = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_fields:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200


if __name__ == '__main__':
    pass
