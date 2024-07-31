from flask import request, jsonify
from model import db, Booking
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

class BookingResource(Resource):
    @jwt_required()
    def get(self, id=None):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return {'message': 'Access denied: Only students can view bookings'}, 403

        if id:
            booking = Booking.query.get(id)
            if not booking:
                return {'message': 'Booking not found'}, 404

            if booking.student_id != current_user['id']:
                return {'message': 'Access denied: This booking is not yours'}, 403

            return booking.serialize()
        
        bookings = Booking.query.filter_by(student_id=current_user['id']).all()
        return [booking.serialize() for booking in bookings]

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return {'message': 'Access denied: Only students can create bookings'}, 403

        data = request.get_json()
        
        check_in = datetime.strptime(data['check_in'], '%Y-%m-%d %H:%M:%S')
        check_out = datetime.strptime(data['check_out'], '%Y-%m-%d %H:%M:%S')

        new_booking = Booking(
            student_id=current_user['id'],
            accommodation_id=data['accommodation_id'],
            check_in=check_in,
            check_out=check_out,
            total_price=data['total_price'],
            status=data['status']
        )
        db.session.add(new_booking)
        db.session.commit()
        return new_booking.serialize(), 201

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return {'message': 'Access denied: Only students can update bookings'}, 403

        data = request.get_json()
        booking = Booking.query.get(id)
        if not booking:
            return {'message': 'Booking not found'}, 404

        if booking.student_id != current_user['id']:
            return {'message': 'Access denied: This booking is not yours'}, 403

        check_in = datetime.strptime(data['check_in'], '%Y-%m-%d %H:%M:%S')
        check_out = datetime.strptime(data['check_out'], '%Y-%m-%d %H:%M:%S')

        booking.student_id = current_user['id']
        booking.accommodation_id = data['accommodation_id']
        booking.check_in = check_in
        booking.check_out = check_out
        booking.total_price = data['total_price']
        booking.status = data['status']
        db.session.commit()
        return booking.serialize()

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user['type'] != 'student':
            return {'message': 'Access denied: Only students can delete bookings'}, 403

        booking = Booking.query.get(id)
        if not booking:
            return {'message': 'Booking not found'}, 404

        if booking.student_id != current_user['id']:
            return {'message': 'Access denied: This booking is not yours'}, 403

        db.session.delete(booking)
        db.session.commit()
        return {'message': 'Booking deleted successfully'}, 200

