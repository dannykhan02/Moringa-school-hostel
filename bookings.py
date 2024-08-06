from flask import request, jsonify, make_response
from model import db, Booking, Accommodation
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

class BookingResource(Resource):
    @jwt_required()
    def get(self, id=None):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return make_response(jsonify({'message': 'Access denied: Only students can view bookings'}), 403)

        if id:
            booking = Booking.query.get(id)
            if not booking:
                return make_response(jsonify({'message': 'Booking not found'}), 404)

            if booking.student_id != current_user['id']:
                return make_response(jsonify({'message': 'Access denied: This booking is not yours'}), 403)

            return make_response(jsonify(booking.serialize()), 200)
        
        bookings = Booking.query.filter_by(student_id=current_user['id']).all()
        return make_response(jsonify([booking.serialize() for booking in bookings]), 200)

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return make_response(jsonify({'message': 'Access denied: Only students can create bookings'}), 403)

        data = request.get_json()
        
        accommodation = Accommodation.query.get(data['accommodation_id'])
        if not accommodation:
            return make_response(jsonify({'message': 'Accommodation not found'}), 404)

        check_in = datetime.strptime(data['check_in'], '%Y-%m-%d %H:%M:%S')
        check_out = check_in + timedelta(days=30)  
        total_price = 30 * accommodation.price_per_night

        
        
        new_booking = Booking(
            student_id=current_user['id'],
            accommodation_id=data['accommodation_id'],
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status='confirmed'
        )
        db.session.add(new_booking)
        db.session.commit()
        return make_response(jsonify(new_booking.serialize()), 201)

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return make_response(jsonify({'message': 'Access denied: Only students can update bookings'}), 403)

        data = request.get_json()
        booking = Booking.query.get(id)
        if not booking:
            return make_response(jsonify({'message': 'Booking not found'}), 404)

        if booking.student_id != current_user['id']:
            return make_response(jsonify({'message': 'Access denied: This booking is not yours'}), 403)

        accommodation = Accommodation.query.get(data['accommodation_id'])
        if not accommodation:
            return make_response(jsonify({'message': 'Accommodation not found'}), 404)

        check_in = datetime.strptime(data['check_in'], '%Y-%m-%d %H:%M:%S')
        check_out = check_in + timedelta(days=30)  

        total_price = 30 * accommodation.price_per_night

        booking.accommodation_id = data['accommodation_id']
        booking.check_in = check_in
        booking.check_out = check_out
        booking.total_price = total_price
        booking.status = data['status']
        db.session.commit()
        return make_response(jsonify(booking.serialize()), 200)

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return make_response(jsonify({'message': 'Access denied: Only students can delete bookings'}), 403)

        booking = Booking.query.get(id)
        if not booking:
            return make_response(jsonify({'message': 'Booking not found'}), 404)

        if booking.student_id != current_user['id']:
            return make_response(jsonify({'message': 'Access denied: This booking is not yours'}), 403)

        db.session.delete(booking)
        db.session.commit()
        return make_response(jsonify({'message': 'Booking deleted successfully'}), 200)
