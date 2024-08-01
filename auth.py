from flask import request
from flask_restful import Resource
from model import db, Student, Host
from flask_jwt_extended import create_access_token
from datetime import timedelta

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


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = Student.query.filter_by(email=email).first()
        user_type = 'student'

        if not user or not user.check_password(password):
            user = Host.query.filter_by(email=email).first()
            user_type = 'host'

            if not user or not user.check_password(password):
                return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(identity={'type': user_type, 'id': user.id}, expires_delta=timedelta(days=30))
        return {'access_token': access_token, 'message': 'Login successful'}, 200
