from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from bookings import BookingResource, HomeResource
from model import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

api.add_resource(BookingResource, '/booking', '/booking/<int:id>')
api.add_resource(HomeResource, '/home')

if __name__ == "__main__":
    app.run(debug=True)
