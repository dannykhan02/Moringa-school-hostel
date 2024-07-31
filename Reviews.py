from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from model import db, Review


class ReviewListResource(Resource):
    def get(self):
        reviews = Review.query.all()
        return [{
            'id': review.id,
            'student_id': review.student_id,
            'accommodation_id': review.accommodation_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews]

    def post(self):
        data = request.get_json()
        student_id = data.get('student_id')
        accommodation_id = data.get('accommodation_id')
        rating = data.get('rating')
        comment = data.get('comment')

        if not student_id or not accommodation_id or not rating:
            return {'message': 'Student ID, accommodation ID, and rating are required'}, 400

        new_review = Review(student_id=student_id, accommodation_id=accommodation_id, rating=rating, comment=comment)
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
    def put(self, id):
        review = Review.query.get(id)

        if review:
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

    def delete(self, id):
        review = Review.query.get(id)

        if review:
            db.session.delete(review)
            db.session.commit()
            return {'message': 'Review deleted'}
        return {'message': 'Review not found'}, 404


class AccommodationReviewResource(Resource):
    def get(self, accommodation_id):
        reviews = Review.query.filter_by(accommodation_id=accommodation_id).all()
        return [{
            'id': review.id,
            'student_id': review.student_id,
            'accommodation_id': review.accommodation_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews]




