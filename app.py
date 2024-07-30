from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
<<<<<<< HEAD
from model import db  
=======
from bookings import BookingResource, HomeResource
from model import db

>>>>>>> origin/edgar
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key' 

api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

<<<<<<< HEAD
from Reviews import ReviewListResource, ReviewResource, AccommodationReviewResource


api.add_resource(ReviewListResource, '/reviews')
api.add_resource(ReviewResource, '/reviews/<int:id>')
api.add_resource(AccommodationReviewResource, '/accommodations/<int:accommodation_id>/reviews')
=======
api.add_resource(BookingResource, '/booking', '/booking/<int:id>')
api.add_resource(HomeResource, '/home')
>>>>>>> origin/edgar

if __name__ == "__main__":
    app.run(debug=True)
