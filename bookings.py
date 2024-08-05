from flask import request, jsonify, make_response
from model import db, Booking, Accommodation
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import stripe

stripe.api_key = 'sk_test_51Pj4YdRxZMXmtnTtXJT976s0PTAAVix1cdQVbtVYcrs83QHit4OecUkmsfnhF31WNa1HS1mCyPha6dTjXyEB7V0n007BNfKiVP'

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
        check_out = check_in + timedelta(days=30)  # Book for a month

        total_price = 30 * accommodation.price_per_night

        if data['amount'] != total_price:
            return make_response(jsonify({'message': 'Payment amount does not match the total price'}), 400)

        payment_method_id = data.get('paymentMethodId')
        currency = data.get('currency', 'kes')
        payment_amount = int(total_price * 100)

        try:
            intent = stripe.PaymentIntent.create(
                amount=payment_amount,
                currency=currency,
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                return_url='https://yourdomain.com/return',
            )
            
            if intent.status != 'succeeded':
                return make_response(jsonify({'message': 'Payment failed', 'status': intent.status}), 400)

        except stripe.error.StripeError as e:
            return make_response(jsonify({'message': 'Payment error', 'error': str(e)}), 400)
        
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
        check_out = check_in + timedelta(days=30)  # Update booking for a month

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
