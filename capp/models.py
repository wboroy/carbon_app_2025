from capp import db
from datetime import datetime
from capp import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Database User
class User(db.Model, UserMixin):
    __tablename__ = "user_table"
    #hver user får en unikt tall
    id = db.Column(db.Integer, primary_key=True)
    #normal profil informasjon
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #lager en forbindelse mellom user og transport entries
    transport = db.relationship('Transport', backref='author', lazy=True)

# Database Transport
class Transport(db.Model):
    __bind_key__ = 'transport'
    __tablename__= 'transport_table'
    id = db.Column(db.Integer, primary_key=True)
    kms = db.Column(db.Float)
    transport = db.Column(db.String)
    fuel = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    co2= db.Column(db.Float)
    ch4= db.Column(db.Float)
    total = db.Column(db.Float)  
    #forbinder hver reise (transport) til den riktige personen
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
