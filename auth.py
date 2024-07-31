from flask import request, jsonify
from flask_restful import Resource
from model import db, Student, Host
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager

class RegisterStudentResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        gender = data.get('gender')

        if Student.query.filter_by(email=email).first():
            return {'message': 'Student already exists'}, 409

        new_student = Student(
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender
        )
        new_student.set_password(password)
        db.session.add(new_student)
        db.session.commit()

        return {'message': 'Student registered successfully'}, 201


class RegisterHostResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if Host.query.filter_by(email=email).first():
            return {'message': 'Host already exists'}, 409

        new_host = Host(
            email=email,
            name=name
        )
        new_host.set_password(password)
        db.session.add(new_host)
        db.session.commit()

        return {'message': 'Host registered successfully'}, 201


class LoginStudentResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        student = Student.query.filter_by(email=email).first()

        if not student or not student.check_password(password):
            return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(identity={'type': 'student', 'id': student.id})
        return {'access_token': access_token, 'message': 'Login successful'}, 200


class LoginHostResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        host = Host.query.filter_by(email=email).first()

        if not host or not host.check_password(password):
            return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(identity={'type': 'host', 'id': host.id})
        return {'access_token': access_token, 'message': 'Login successful'}, 200

