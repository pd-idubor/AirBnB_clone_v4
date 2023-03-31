#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_by_cities(city_id=None):
    """Retrieves the list of all Place objects of a City"""
    if (city_id):
        city = storage.get("City", city_id)
        if city is not None:
            places = [place.to_dict() for place in city.places]
            return (jsonify(places), 200)
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id=None):
    """Retrieves Place objects"""
    if (place_id):
        place = storage.get("Place", place_id)
        if place is not None:
            return (jsonify(place.to_dict()), 200)
        abort(404)


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_places(place_id=None):
    """Deletes a Place object"""
    if (place_id):
        place = storage.get("Place", place_id)
        if place is not None:
            storage.delete(place)
            storage.save()
            return (jsonify({}), 200)
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def create_places(city_id=None):
    """Creates a City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    user_id = data.get("user_id")
    if user_id is None:
        return (jsonify({"error": "Missing user_id"}), 400)
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    name = data.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    place = Place()
    place.city_id = city.id
    for key, val in data.items():
        setattr(place, key, val)

    place.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=["PUT"],
                 strict_slashes=False)
def update_places(place_id):
    """Updates a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)

    place.save()
    return (jsonify(place.to_dict()), 200)
