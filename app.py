from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from model import db
from accommodation import AccommodationResource, AccommodationAmenityResource
from amenity import AmenityResource
from Reviews import ReviewListResource, ReviewResource, AccommodationReviewResource
from bookings import BookingResource, HomeResource
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Optional: Remove if JWT is not used

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

api.add_resource(BookingResource, '/booking', '/booking/<int:id>')
api.add_resource(HomeResource, '/home')
api.add_resource(AccommodationResource, '/accommodations', '/accommodations/<int:id>')
api.add_resource(AccommodationAmenityResource, '/accommodations/<int:accommodation_id>/amenities')
api.add_resource(AmenityResource, '/amenities', '/amenities/<int:id>')
api.add_resource(ReviewListResource, '/reviews')
api.add_resource(ReviewResource, '/reviews/<int:id>')
api.add_resource(AccommodationReviewResource, '/accommodations/<int:accommodation_id>/reviews')



if __name__ == '__main__':
    app.run(debug=True)
