#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def cities_by_states(state_id=None):
    """Retrieves the list of all City objects of a State"""
    if (state_id):
        state = storage.get("State", state_id)
        if state is not None:
            cities = [city.to_dict() for city in state.cities]
            return jsonify(cities)
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id=None):
    """Retrieves City objects"""
    if (city_id):
        city = storage.get("City", city_id)
        if city is not None:
            return jsonify(city.to_dict())
        abort(404)


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_cities(city_id=None):
    """Deletes a City object"""
    if (city_id):
        city = storage.get("City", city_id)
        if city is not None:
            storage.delete(city)
            storage.save()
            return (jsonify({}), 200)
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def post_cities(state_id=None):
    """Creates a City"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)
    name = data.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    state = storage.get("State", state_id)
    if state is not None:
        new_city = City()
        new_city.state_id = state_id
        new_city.name = name
        new_city.save()
        return (jsonify(new_city.to_dict()), 201)
    abort(404)


@app_views.route('cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_cities(city_id):
    """Updates a City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)

    city.save()
    return (jsonify(city.to_dict()), 200)
