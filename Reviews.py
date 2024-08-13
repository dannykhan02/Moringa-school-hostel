from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from model import db, Review

class ReviewListResource(Resource):
    def get(self):
        reviews = Review.query.all()
        return [{
            'id': review.id,
            'student_id': review.student_id,
            'location': review.location,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews]

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return {'message': 'Access denied: Only students can create reviews'}, 403

        data = request.get_json()
        location = data.get('location')
        rating = data.get('rating')
        comment = data.get('comment')

        if not location or not rating:
            return {'message': 'Location and rating are required'}, 400

        new_review = Review(
            student_id=current_user['id'],
            location=location,
            rating=rating,
            comment=comment
        )
        db.session.add(new_review)
        db.session.commit()

        return {
            'id': new_review.id,
            'student_id': new_review.student_id,
            'location': new_review.location,
            'rating': new_review.rating,
            'comment': new_review.comment
        }, 201

class ReviewResource(Resource):
    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return {'message': 'Access denied: Only students can update reviews'}, 403

        review = Review.query.get(id)
        if review:
            if review.student_id != current_user['id']:
                return {'message': 'Access denied: This review is not yours'}, 403

            data = request.get_json()
            review.rating = data.get('rating', review.rating)
            review.comment = data.get('comment', review.comment)
            db.session.commit()

            return {
                'id': review.id,
                'student_id': review.student_id,
                'location': review.location,
                'rating': review.rating,
                'comment': review.comment
            }, 200

        return {'message': 'Review not found'}, 404

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return {'message': 'Access denied: Only students can delete reviews'}, 403

        review = Review.query.get(id)
        if review:
            if review.student_id != current_user['id']:
                return {'message': 'Access denied: This review is not yours'}, 403

            db.session.delete(review)
            db.session.commit()
            return {'message': 'Review deleted'}, 200

        return {'message': 'Review not found'}, 404

class LocationReviewResource(Resource):
    def get(self, location):
        reviews = Review.query.filter_by(location=location).all()
        return [{
            'id': review.id,
            'student_id': review.student_id,
            'location': review.location,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews]
