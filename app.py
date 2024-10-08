from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from model import db
from accommodation import AccommodationResource, AccommodationAmenityResource
from Reviews import ReviewListResource, ReviewResource, LocationReviewResource
from bookings import BookingResource
from amenity import AmenityResource
from auth import RegisterStudentResource, RegisterHostResource, LoginStudentResource, LoginHostResource, UserRoleResource, PasswordResetResource
import os
app = Flask(__name__)
api = Api(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'kejani'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://nest_oed3_user:K9fC5GjgqcoLRm13nuoZ3eFXZGqaOR89@dpg-cqtl7pij1k6c738obpp0-a.ohio-postgres.render.com/nest_oed3')

db.init_app(app)


api.add_resource(RegisterStudentResource, '/auth/register/student')
api.add_resource(RegisterHostResource, '/auth/register/host')
api.add_resource(LoginStudentResource, '/auth/login/student')
api.add_resource(LoginHostResource, '/auth/login/host')
api.add_resource(UserRoleResource, '/auth/user/role')
api.add_resource(PasswordResetResource, '/auth/reset/password')


api.add_resource(BookingResource, '/booking', '/booking/<int:id>')


api.add_resource(ReviewListResource, '/reviews')
api.add_resource(ReviewResource, '/reviews/<int:id>')
api.add_resource(LocationReviewResource, '/locations/<string:location>/reviews')


api.add_resource(AccommodationResource, '/accommodations', '/accommodations/<int:id>')
api.add_resource(AccommodationAmenityResource, '/accommodations/<int:accommodation_id>/amenities')


api.add_resource(AmenityResource, '/amenities', '/amenities/<int:id>')


with app.test_request_context():
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

if __name__ == '__main__':
    app.run(debug=True)