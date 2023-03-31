#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def all_states(state_id=None):
    """Retrieves the list of all State objects"""
    if (state_id):
        state = storage.get("State", state_id)
        if state is not None:
            return jsonify(state.to_dict())
        abort(404)

    new_list = []
    states = storage.all("State")
    for state in states.values():
        new_list.append(state.to_dict())
    return jsonify(new_list)


@app_views.route('/states/<state_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete(state_id=None):
    """Deletes a State object"""
    if (state_id):
        state = storage.get("State", state_id)
        if state is not None:
            storage.delete(state)
            storage.save()
            return (jsonify({}))
        abort(404)


@app_views.route('/states', methods=["POST"],
                 strict_slashes=False)
def post_states():
    """Creates a State"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)
    name = data.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new_state = State(**data)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"],
                 strict_slashes=False)
def update_states(state_id):
    """Updates a State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)

    state.save()
    return (jsonify(state.to_dict()), 200)
