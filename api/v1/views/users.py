#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def all_users(user_id=None):
    """Retrieves the list of all User objects"""
    if (user_id):
        user = storage.get("User", user_id)
        if user is not None:
            return jsonify(user.to_dict())
        abort(404)

    new_list = []
    users = storage.all("User")
    for user in users.values():
        new_list.append(user.to_dict())
    return jsonify(new_list)


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_users(user_id=None):
    """Deletes a User object"""
    if (user_id):
        user = storage.get("User", user_id)
        if user is not None:
            storage.delete(user)
            storage.save()
            return (jsonify({}), 200)
        abort(404)


@app_views.route('/users', methods=["POST"],
                 strict_slashes=False)
def create_users():
    """Creates a User"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)
    email = data.get("email")
    if email is None:
        return (jsonify({"error": "Missing email"}), 400)
    password = data.get("password")
    if password is None:
        return (jsonify({"error": "Missing password"}), 400)

    new = User()
    for key, value in data.items():
        setattr(new, key, value)
    new.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def update_users(user_id):
    """Updates a User"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)

    user.save()
    return (jsonify(user.to_dict()), 200)
