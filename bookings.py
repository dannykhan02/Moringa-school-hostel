from flask import request, jsonify, make_response
from model import db, Booking, Accommodation
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mpesa_payment import initiate_mpesa_payment

class BookingResource(Resource):
    @jwt_required()
    def get(self, id=None):
        current_user = get_jwt_identity()

        if current_user['type'] == 'student':
            if id:
                booking = Booking.query.get(id)
                if not booking:
                    return make_response(jsonify({'message': 'Booking not found'}), 404)
                if booking.student_id != current_user['id']:
                    return make_response(jsonify({'message': 'Access denied: This booking is not yours'}), 403)
                return make_response(jsonify(booking.serialize()), 200)

            bookings = Booking.query.filter_by(student_id=current_user['id']).all()
            return make_response(jsonify([booking.serialize() for booking in bookings]), 200)

        elif current_user['type'] == 'host':
            accommodations = Accommodation.query.filter_by(host_id=current_user['id']).all()
            if not accommodations:
                return make_response(jsonify({'message': 'No accommodations found for this host'}), 404)
            accommodation_ids = [accommodation.id for accommodation in accommodations]
            bookings = Booking.query.filter(Booking.accommodation_id.in_(accommodation_ids)).all()
            return make_response(jsonify([booking.serialize() for booking in bookings]), 200)

        return make_response(jsonify({'message': 'Access denied: Invalid user type'}), 403)

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return make_response(jsonify({'message': 'Access denied: Only students can create bookings'}), 403)

        data = request.get_json()
        accommodation = Accommodation.query.get(data['accommodation_id'])
        if not accommodation:
            return make_response(jsonify({'message': 'Accommodation not found'}), 404)

        try:
            check_in = datetime.strptime(data['check_in'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return make_response(jsonify({'message': 'Invalid date format for check-in'}), 400)
        
        check_out = check_in + timedelta(days=30)
        total_price = 30 * accommodation.price_per_night
        total_price = int(total_price)

        phone_number = data.get('phone_number')
        if not phone_number:
            return make_response(jsonify({'message': 'Phone number is required for payment'}), 400)

        payment_response = initiate_mpesa_payment(total_price, phone_number)
        if payment_response.status_code != 200:
            return make_response(jsonify({'message': 'Payment initiation failed', 'details': payment_response.text}), 400)

        payment_result = payment_response.json()
        if payment_result.get('ResponseCode') != '0':
            return make_response(jsonify({'message': 'Payment failed', 'details': payment_result}), 400)

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

        try:
            check_in = datetime.strptime(data['check_in'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return make_response(jsonify({'message': 'Invalid date format for check-in'}), 400)
        
        check_out = check_in + timedelta(days=30)
        total_price = 30 * accommodation.price_per_night
        total_price = int(total_price)

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
