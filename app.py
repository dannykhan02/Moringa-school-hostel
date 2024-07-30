from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from model import db
from accommodation import AccommodationResource, AccommodationAmenityResource
from amenity import AmenityResource

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key' 



db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


from Reviews import ReviewListResource, ReviewResource, AccommodationReviewResource


api.add_resource(ReviewListResource, '/reviews')
api.add_resource(ReviewResource, '/reviews/<int:id>')
api.add_resource(AccommodationReviewResource, '/accommodations/<int:accommodation_id>/reviews')

api.add_resource(AccommodationResource, '/accommodations', '/accommodations/<int:id>')
api.add_resource(AccommodationAmenityResource, '/accommodations/<int:accommodation_id>/amenities')
api.add_resource(AmenityResource, '/amenities', '/amenities/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
