from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from model import db
from accommodation import AccommodationResource, AccommodationAmenityResource
from amenity import AmenityResource

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


api.add_resource(AccommodationResource, '/accommodations', '/accommodations/<int:id>')
api.add_resource(AccommodationAmenityResource, '/accommodations/<int:accommodation_id>/amenities')
api.add_resource(AmenityResource, '/amenities', '/amenities/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
