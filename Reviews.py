from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from model import db, Review

class ReviewListResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        # if current_user['type'] != 'student':
        #     return {'message': 'Access denied: Only students can view reviews'}, 403

        reviews = Review.query.all()
        return [{
            'id': review.id,
            'student_id': review.student_id,
            'accommodation_id': review.accommodation_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews]

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return {'message': 'Access denied: Only students can create reviews'}, 403

        data = request.get_json()
        accommodation_id = data.get('accommodation_id')
        rating = data.get('rating')
        comment = data.get('comment')

        if not accommodation_id or not rating:
            return {'message': 'Accommodation ID and rating are required'}, 400

        new_review = Review(
            student_id=current_user['id'],
            accommodation_id=accommodation_id,
            rating=rating,
            comment=comment
        )
        db.session.add(new_review)
        db.session.commit()

        return {
            'id': new_review.id,
            'student_id': new_review.student_id,
            'accommodation_id': new_review.accommodation_id,
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
                'accommodation_id': review.accommodation_id,
                'rating': review.rating,
                'comment': review.comment
            }
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
            return {'message': 'Review deleted successfully'}
        return {'message': 'Review not found'}, 404

class AccommodationReviewResource(Resource):
    @jwt_required()
    def get(self, accommodation_id):
        reviews = Review.query.filter_by(accommodation_id=accommodation_id).all()
        return [{
            'id': review.id,
            'student_id': review.student_id,
            'accommodation_id': review.accommodation_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews]
