#!/usr/bin/python3
"""places_reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from datetime import datetime
import uuid


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                    strict_slashes=False)
def get_all_reviews(place_id):
    """ Get all reviews for a place
    
        Return:
        List of reviews for a place
    """
    place = storage.get(Place, place_id)
    if place:
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)
    else:
        abort(404)
        

@app_views.route('/reviews/<review_id>', methods=['GET'],
                    strict_slashes=False)
def get_review(review_id):
    """ Get a review by id
    
        Return:
        Review with the given id
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete a review by id
    
        Return:
        Empty JSON response
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                    strict_slashes=False)
def post_review(place_id):
    """ Create a new review for a place
    
        Return:
        Newly created review
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, "Missing user_id")
    if 'text' not in request.get_json():
        abort(400, "Missing text")
    user_id = request.get_json()['user_id']
    text = request.get_json()['text']
    place = storage.get(Place, place_id)
    if place:
        new_review = Review(place_id=place_id, user_id=user_id, text=text,
                            created_at=datetime.now(), updated_at=datetime.now())
        new_review.id = str(uuid.uuid4())
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ Update a review by id
    
        Return:
        Updated review
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if review:
        if 'user_id' in request.get_json():
            review.user_id = request.get_json()['user_id']
        if 'text' in request.get_json():
            review.text = request.get_json()['text']
        review.updated_at = datetime.now()
        storage.save()
        return jsonify(review.to_dict())
    else:
        abort(404)
