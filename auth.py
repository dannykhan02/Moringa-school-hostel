from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from model import db, Student, Host
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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


class LoginStudentResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        student = Student.query.filter_by(email=email).first()

        if not student or not student.check_password(password):
            return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(
            identity={'type': 'student', 'id': student.id, 'first_name': student.first_name, 'last_name': student.last_name, 'email': student.email},
            expires_delta=timedelta(days=30)
        )
        return {'access_token': access_token, 'message': 'Login successful'}, 200


class LoginHostResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        host = Host.query.filter_by(email=email).first()

        if not host or not host.check_password(password):
            return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(
            identity={'type': 'host', 'id': host.id, 'name': host.name, 'email': host.email},
            expires_delta=timedelta(days=30)
        )
        return {'access_token': access_token, 'message': 'Login successful'}, 200


class UserRoleResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user['type'] == 'student':
            user = Student.query.get(current_user['id'])
            if not user:
                return {'message': 'User not found'}, 404
            user_info = {
                'role': 'student',
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender
            }
        elif current_user['type'] == 'host':
            user = Host.query.get(current_user['id'])
            if not user:
                return {'message': 'User not found'}, 404
            user_info = {
                'role': 'host',
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
        else:
            return {'message': 'Invalid user role'}, 400

        return user_info, 200


class PasswordResetResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        new_password = data.get('new_password')

        if not email or not new_password:
            return {'message': 'Email and new password are required'}, 400

        student = Student.query.filter_by(email=email).first()
        host = Host.query.filter_by(email=email).first()

        user = student if student else host
        if not user:
            return {'message': 'User not found'}, 404

        user.password_hash = generate_password_hash(new_password, method='scrypt')
        db.session.commit()

        return {'message': 'Password reset successfully'}, 200