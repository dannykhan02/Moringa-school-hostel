from flask import request, jsonify
from flask_restful import Resource
from model import db, Accommodation, Amenity, AccommodationAmenity

class AccommodationResource(Resource):
    def get(self, id=None):
        if id:
            accommodation = Accommodation.query.get(id)
            if not accommodation:
                return {'message': 'Accommodation not found'}, 404
            return jsonify(accommodation.as_dict())
        accommodations = Accommodation.query.all()
        return jsonify([accommodation.as_dict() for accommodation in accommodations])

    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        location = data.get('location')
        price_per_night = data.get('price_per_night')
        host_id = data.get('host_id')

        if not all([title, description, location, price_per_night, host_id]):
            return {'message': 'Missing required fields'}, 400

        new_accommodation = Accommodation(
            title=title,
            description=description,
            location=location,
            price_per_night=price_per_night,
            host_id=host_id
        )
        db.session.add(new_accommodation)
        db.session.commit()
        return jsonify(new_accommodation.as_dict()), 201

    def put(self, id):
        data = request.get_json()
        accommodation = Accommodation.query.get(id)
        if not accommodation:
            return {'message': 'Accommodation not found'}, 404

        accommodation.title = data.get('title', accommodation.title)
        accommodation.description = data.get('description', accommodation.description)
        accommodation.location = data.get('location', accommodation.location)
        accommodation.price_per_night = data.get('price_per_night', accommodation.price_per_night)
        db.session.commit()
        return jsonify(accommodation.as_dict())

    def delete(self, id):
        accommodation = Accommodation.query.get(id)
        if not accommodation:
            return {'message': 'Accommodation not found'}, 404

        db.session.delete(accommodation)
        db.session.commit()
        return '', 204

class AccommodationAmenityResource(Resource):
    def post(self, accommodation_id):
        data = request.get_json()
        amenity_id = data.get('amenity_id')

        if not amenity_id:
            return {'message': 'Missing amenity_id'}, 400

        accommodation = Accommodation.query.get(accommodation_id)
        if not accommodation:
            return {'message': 'Accommodation not found'}, 404

        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404

        accommodation_amenity = AccommodationAmenity(
            accommodation_id=accommodation_id,
            amenity_id=amenity_id
        )
        db.session.add(accommodation_amenity)
        db.session.commit()
        return {'message': 'Amenity added to accommodation'}, 201

    def get(self, accommodation_id):
        accommodation = Accommodation.query.get(accommodation_id)
        if not accommodation:
            return {'message': 'Accommodation not found'}, 404

        amenities = AccommodationAmenity.query.filter_by(accommodation_id=accommodation_id).all()
        amenity_list = [{'id': amenity.amenity.id, 'name': amenity.amenity.name} for amenity in amenities]
        return jsonify(amenity_list)
