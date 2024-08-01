from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from model import db, Accommodation, Amenity, AccommodationAmenity

class AccommodationResource(Resource):
    def get(self, id=None):
        if id:
            accommodation = Accommodation.query.get(id)
            if not accommodation:
                return make_response(jsonify({'message': 'Accommodation not found'}), 404)
            return make_response(jsonify(accommodation.as_dict()), 200)
        accommodations = Accommodation.query.all()
        return make_response(jsonify([accommodation.as_dict() for accommodation in accommodations]), 200)

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['type'] != 'host':
            return make_response(jsonify({'message': 'Access forbidden: Insufficient role'}), 403)

        data = request.get_json()
        if not isinstance(data, list):
            return make_response(jsonify({'message': 'Expected a list of accommodations'}), 400)

        new_accommodations = []
        for accommodation_data in data:
            title = accommodation_data.get('title')
            description = accommodation_data.get('description')
            location = accommodation_data.get('location')
            price_per_night = accommodation_data.get('price_per_night')
            number_of_rooms = accommodation_data.get('number_of_rooms')
            number_of_students = accommodation_data.get('number_of_students')
            host_id = current_user['id']

            if not all([title, description, location, price_per_night, number_of_rooms, number_of_students, host_id]):
                return make_response(jsonify({'message': 'Missing required fields in one or more accommodations'}), 400)

            new_accommodation = Accommodation(
                title=title,
                description=description,
                location=location,
                price_per_night=price_per_night,
                number_of_rooms=number_of_rooms,
                number_of_students=number_of_students,
                host_id=host_id
            )
            db.session.add(new_accommodation)
            new_accommodations.append(new_accommodation)

        db.session.commit()
        return make_response(jsonify([accommodation.as_dict() for accommodation in new_accommodations]), 201)

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        if current_user['type'] != 'host':
            return make_response(jsonify({'message': 'Access forbidden: Insufficient role'}), 403)

        accommodation = Accommodation.query.get(id)
        if not accommodation:
            return make_response(jsonify({'message': 'Accommodation not found'}), 404)

        if accommodation.host_id != current_user['id']:
            return make_response(jsonify({'message': 'Access forbidden: You do not own this accommodation'}), 403)

        data = request.get_json()
        accommodation.title = data.get('title', accommodation.title)
        accommodation.description = data.get('description', accommodation.description)
        accommodation.location = data.get('location', accommodation.location)
        accommodation.price_per_night = data.get('price_per_night', accommodation.price_per_night)
        accommodation.number_of_rooms = data.get('number_of_rooms', accommodation.number_of_rooms)
        accommodation.number_of_students = data.get('number_of_students', accommodation.number_of_students)
        db.session.commit()
        return make_response(jsonify(accommodation.as_dict()), 200)

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user['type'] != 'host':
            return make_response(jsonify({'message': 'Access forbidden: Insufficient role'}), 403)

        accommodation = Accommodation.query.get(id)
        if not accommodation:
            return make_response(jsonify({'message': 'Accommodation not found'}), 404)

        if accommodation.host_id != current_user['id']:
            return make_response(jsonify({'message': 'Access forbidden: You do not own this accommodation'}), 403)

        db.session.delete(accommodation)
        db.session.commit()
        return make_response('', 204)

class AccommodationAmenityResource(Resource):
    def post(self, accommodation_id):
        data = request.get_json()
        amenity_id = data.get('amenity_id')

        if not amenity_id:
            return make_response(jsonify({'message': 'Missing amenity_id'}), 400)

        accommodation = Accommodation.query.get(accommodation_id)
        if not accommodation:
            return make_response(jsonify({'message': 'Accommodation not found'}), 404)

        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return make_response(jsonify({'message': 'Amenity not found'}), 404)

        accommodation_amenity = AccommodationAmenity(
            accommodation_id=accommodation_id,
            amenity_id=amenity_id
        )
        db.session.add(accommodation_amenity)
        db.session.commit()
        return make_response(jsonify({'message': 'Amenity added to accommodation'}), 201)

    def get(self, accommodation_id):
        accommodation = Accommodation.query.get(accommodation_id)
        if not accommodation:
            return make_response(jsonify({'message': 'Accommodation not found'}), 404)

        amenities = AccommodationAmenity.query.filter_by(accommodation_id=accommodation_id).all()
        amenity_list = [{'id': amenity.amenity.id, 'name': amenity.amenity.name} for amenity in amenities]
        return make_response(jsonify(amenity_list), 200)
