from flask import request, jsonify
from model import db, Booking
from datetime import datetime
from flask_jwt_extended import jwt_required
from flask_restful import Resource

class HomeResource(Resource):
    def get(self):
        return {'message': 'Hello, World!'}
from flask import request, jsonify
from model import db, Booking
from datetime import datetime
from flask_restful import Resource

class BookingResource(Resource):
    def get(self, id=None):
        if id:
            booking = Booking.query.get(id)
            if not booking:
                return {'message': 'Booking not found'}, 404
            return booking.serialize()
        bookings = Booking.query.all()
        return [booking.serialize() for booking in bookings]

    def post(self):
        data = request.get_json()
        
        check_in = datetime.strptime(data['check_in'], '%Y-%m-%d %H:%M:%S')
        check_out = datetime.strptime(data['check_out'], '%Y-%m-%d %H:%M:%S')
        
        new_booking = Booking(
            student_id=data['student_id'],
            accommodation_id=data['accommodation_id'],
            check_in=check_in, 
            check_out=check_out, 
            total_price=data['total_price'], 
            status=data['status']
        )
        db.session.add(new_booking)
        db.session.commit()
        return new_booking.serialize(), 201

    def put(self, id):
        data = request.get_json()
        booking = Booking.query.get(id)
        if not booking:
            return {'message': 'Booking not found'}, 404

        # Convert date strings to datetime objects
        check_in = datetime.strptime(data['check_in'], '%Y-%m-%d %H:%M:%S')
        check_out = datetime.strptime(data['check_out'], '%Y-%m-%d %H:%M:%S')
        
        booking.student_id = data['student_id']
        booking.accommodation_id = data['accommodation_id']
        booking.check_in = check_in
        booking.check_out = check_out
        booking.total_price = data['total_price']
        booking.status = data['status']
        db.session.commit()
        return booking.serialize()
        
    def delete(self, id):
        booking = Booking.query.get(id)
        if not booking:
            return {'message': 'Booking not found'}, 404

        db.session.delete(booking)
        db.session.commit()
        return {'message': 'Booking deleted successfully'}, 200


