from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)  
    

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        if user.role == 'user':
            access_token = create_access_token(identity={'email': user.email, 'role': 'user'})
            return jsonify(message="Login successful!", access_token=access_token), 200
        else:
            return jsonify(message="This endpoint is for users only."), 403
    return jsonify(message="Invalid email or password"), 401

@app.route('/api/host-login', methods=['POST'])
def host_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        if user.role == 'host':
            access_token = create_access_token(identity={'email': user.email, 'role': 'host'})
            return jsonify(message="Login successful!", access_token=access_token), 200
        else:
            return jsonify(message="This endpoint is for hosts only."), 403
    return jsonify(message="Invalid email or password"), 401

if __name__ == '__main__':
    app.run(debug=True)
