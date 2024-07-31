from flask import request, jsonify
from flask_restful import Resource
from model import db, Amenity

class AmenityResource(Resource):
    def get(self, id=None):
        if id:
            amenity = Amenity.query.get(id)
            if not amenity:
                return {'message': 'Amenity not found'}, 404
            return jsonify(amenity.as_dict())
        amenities = Amenity.query.all()
        return jsonify([amenity.as_dict() for amenity in amenities])
    
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not name:
            return {'message': 'Missing required fields'}, 400

        new_amenity = Amenity(
            name=name,
            description=description
        )
        db.session.add(new_amenity)
        db.session.commit()
        return jsonify(new_amenity.as_dict()), 201

    def put(self, id):
        data = request.get_json()
        amenity = Amenity.query.get(id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404

        amenity.name = data.get('name', amenity.name)
        amenity.description = data.get('description', amenity.description)
        db.session.commit()
        return jsonify(amenity.as_dict())

    def delete(self, id):
        amenity = Amenity.query.get(id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404

        db.session.delete(amenity)
        db.session.commit()
        return '', 204
