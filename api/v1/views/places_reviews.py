#!/usr/bin/python3
"""
    Handles default RESTFul API actions
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review(place_id=None):
    """Retrieves the list of all Review objects of a Place"""
    if (place_id):
        place = storage.get("Place", place_id)
        if place is not None:
            reviews = [review.to_dict() for review in place.reviews]
            return jsonify(reviews)
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id=None):
    """Retrieves Review objects"""
    if (review_id):
        review = storage.get("Review", review_id)
        if review is not None:
            return jsonify(review.to_dict())
        abort(404)


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Deletes a Review object"""
    if (review_id):
        review = storage.get("Review", review_id)
        if review is not None:
            storage.delete(review)
            storage.save()
            return (jsonify({}), 200)
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def create_review(place_id=None):
    """Creates a Review"""
    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    user_id = data.get("user_id")
    if user_id is None:
        return (jsonify({"error": "Missing user_id"}), 400)

    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    text = data.get("text")
    if text is None:
        return (jsonify({"error": "Missing text"}), 400)

    new = Review()
    new.place_id = place.id

    for key, val in data.items():
        setattr(new, key, val)
    new.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if (data is None):
        return (jsonify({"error": "Not a JSON"}), 400)

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)

    review.save()
    return (jsonify(review.to_dict()), 200)
