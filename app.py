from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from model import db
from accommodation import AccommodationResource, AccommodationAmenityResource
from Reviews import ReviewListResource, ReviewResource, AccommodationReviewResource
from bookings import BookingResource
from amenity import AmenityResource
from auth import RegisterStudentResource, RegisterHostResource, LoginStudentResource, LoginHostResource
from payment import PaymentResource, VerifyPaymentResource

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'you never walk alone'

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

jwt = JWTManager(app)

api.add_resource(RegisterStudentResource, '/auth/register/student')
api.add_resource(RegisterHostResource, '/auth/register/host')
api.add_resource(LoginStudentResource, '/auth/login/student')
api.add_resource(LoginHostResource, '/auth/login/host')

api.add_resource(BookingResource, '/booking', '/booking/<int:id>')

api.add_resource(ReviewListResource, '/reviews')
api.add_resource(ReviewResource, '/reviews/<int:id>')
api.add_resource(AccommodationReviewResource, '/accommodations/<int:accommodation_id>/reviews')

api.add_resource(AccommodationResource, '/accommodations', '/accommodations/<int:id>')
api.add_resource(AccommodationAmenityResource, '/accommodations/<int:accommodation_id>/amenities')
api.add_resource(AmenityResource, '/amenities', '/amenities/<int:id>')

# Adding the Payment Resource
api.add_resource(PaymentResource, '/payments')

# Adding the Verify Payment Resource
api.add_resource(VerifyPaymentResource, '/verify_payment/<string:charge_id>')

if __name__ == '__main__':
    app.run(debug=True)
