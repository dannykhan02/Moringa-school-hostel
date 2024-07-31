from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from model import db, Amenity

class AmenityResource(Resource):
    def get(self, id=None):
        if id:
            amenity = Amenity.query.get(id)
            if not amenity:
                return make_response(jsonify({'message': 'Amenity not found'}), 404)
            return make_response(jsonify(amenity.as_dict()), 200)
        amenities = Amenity.query.all()
        return make_response(jsonify([amenity.as_dict() for amenity in amenities]), 200)

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['type'] != 'host':
            return make_response(jsonify({'message': 'Access forbidden: Insufficient role'}), 403)

        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not name:
            return make_response(jsonify({'message': 'Missing required fields'}), 400)

        new_amenity = Amenity(
            name=name,
            description=description
        )
        db.session.add(new_amenity)
        db.session.commit()
        return make_response(jsonify(new_amenity.as_dict()), 201)

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        if current_user['type'] != 'host':
            return make_response(jsonify({'message': 'Access forbidden: Insufficient role'}), 403)

        amenity = Amenity.query.get(id)
        if not amenity:
            return make_response(jsonify({'message': 'Amenity not found'}), 404)

        data = request.get_json()
        amenity.name = data.get('name', amenity.name)
        amenity.description = data.get('description', amenity.description)
        db.session.commit()
        return make_response(jsonify(amenity.as_dict()), 200)

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user['type'] != 'host':
            return make_response(jsonify({'message': 'Access forbidden: Insufficient role'}), 403)

        amenity = Amenity.query.get(id)
        if not amenity:
            return make_response(jsonify({'message': 'Amenity not found'}), 404)

        db.session.delete(amenity)
        db.session.commit()
        return make_response('', 204)
