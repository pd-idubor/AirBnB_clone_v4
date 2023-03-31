#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def all_amenities(amenity_id=None):
    """Retrieves the list of all Amenity objects"""
    if (amenity_id):
        amenity = storage.get("Amenity", amenity_id)
        if amenity is not None:
            return jsonify(amenity.to_dict())
        abort(404)

    new_list = []
    amenities = storage.all("Amenity")
    for amenity in amenities.values():
        new_list.append(amenity.to_dict())
    return jsonify(new_list)


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenities(amenity_id=None):
    """Deletes an Amenity  object"""
    if (amenity_id):
        amenity = storage.get("Amenity", amenity_id)
        if amenity is not None:
            storage.delete(amenity)
            storage.save()
            return (jsonify({}))
        abort(404)


@app_views.route('/amenities', methods=["POST"],
                 strict_slashes=False)
def create_amenities():
    """Creates an Amenity"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)
    name = data.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    new = Amenity()
    new.name = name
    new.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """Updates a State"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)

    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
