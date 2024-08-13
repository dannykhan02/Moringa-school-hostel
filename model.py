from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bookings = db.relationship('Booking', backref='student', lazy=True, cascade="all, delete-orphan", passive_deletes=True)
    reviews = db.relationship('Review', backref='student', lazy=True, cascade="all, delete-orphan", passive_deletes=True)
    student_amenities = db.relationship('StudentAmenity', back_populates='student', cascade="all, delete-orphan", passive_deletes=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'email': self.email
        }

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    accommodations = db.relationship('Accommodation', backref='host', lazy=True, cascade="all, delete-orphan", passive_deletes=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Accommodation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_students = db.Column(db.Integer, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id', ondelete="CASCADE"), nullable=False)
    bookings = db.relationship('Booking', backref='accommodation', lazy=True, cascade="all, delete-orphan", passive_deletes=True)
    amenities = db.relationship('AccommodationAmenity', back_populates='accommodation', cascade="all, delete-orphan", passive_deletes=True)

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'price_per_night': self.price_per_night,
            'number_of_rooms': self.number_of_rooms,
            'number_of_students': self.number_of_students,
            'host_id': self.host_id
        }

class Amenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    description = db.Column(db.Text, nullable=True)
    student_amenities = db.relationship('StudentAmenity', back_populates='amenity', cascade="all, delete-orphan", passive_deletes=True)
    accommodations = db.relationship('AccommodationAmenity', back_populates='amenity', cascade="all, delete-orphan", passive_deletes=True)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="CASCADE"), nullable=False)
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodation.id', ondelete="CASCADE"), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def serialize(self):
        student = self.student  
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_first_name': student.first_name, 
            'student_last_name': student.last_name,
            'accommodation_id': self.accommodation_id,
            'check_in': self.check_in.strftime('%d/%m/%Y'),
            'check_out': self.check_out.strftime('%d/%m/%Y'),
            'total_price': self.total_price,
            'status': self.status
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="CASCADE"), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    def as_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'location': self.location,
            'rating': self.rating,
            'comment': self.comment
        }

class StudentAmenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="CASCADE"), nullable=False)
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenity.id', ondelete="CASCADE"), nullable=False)
    preference_level = db.Column(db.String(50), nullable=True)
    student = db.relationship('Student', back_populates='student_amenities')
    amenity = db.relationship('Amenity', back_populates='student_amenities')

    def as_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'amenity_id': self.amenity_id,
            'preference_level': self.preference_level
        }

class AccommodationAmenity(db.Model):
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodation.id', ondelete="CASCADE"), primary_key=True)
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenity.id', ondelete="CASCADE"), primary_key=True)
    accommodation = db.relationship('Accommodation', back_populates='amenities')
    amenity = db.relationship('Amenity', back_populates='accommodations')

    def as_dict(self):
        return {
            'accommodation_id': self.accommodation_id,
            'amenity_id': self.amenity_id
        }
