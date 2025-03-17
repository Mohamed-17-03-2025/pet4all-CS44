from p4a import db, login_manager
from p4a import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)#This will serve as the primary key for the Pet table.
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    price = db.Column(db.String(15))
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))#Reference ID found in the User model.
    seller = db.relationship('User', backref='pets_listed', lazy=True)
    seller_phone = db.Column(db.String(20))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=True, default=False)
    pets = db.relationship('Pet', backref='owner', lazy=True)
    rating = db.Column(db.Float, default=0)
    reviews = db.Column(db.String(100), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    total_ratings = db.Column(db.Integer, default=0)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_password):
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def verify_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Accessory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seller = db.relationship('User', backref='accessories_sold', lazy=True)

    def __repr__(self):
        return f"Accessory('{self.name}', '{self.price}')"


