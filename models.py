from sqlalchemy import func
from website import db  # imports a db from within the same package
from flask_login import UserMixin  # helps users login

# model.py purpose is to create the db models
# model.py purpose also is for what the db will look like


class Note(db.Model):  # this table will store notes for each user
    id = db.Column(db.Integer, primary_key=True)  # the id's will be incremented automatically
    data = db.Column(db.String(10000))  # basically a note
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # this will specify the date for us automatically
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # will allow one user to have many notes
    # line above allows us to figure out what user made notes by seeing user id
    # ('user.id) is the ('tableName.primaryKey')


class User(db.Model, UserMixin):  # creates a db, then inherits from the db(db.model), then
    # below defines the columns to be used in the db
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)  # unique true means no user can have the same email
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note')  # allows us to see all the notes

