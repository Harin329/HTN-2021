import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }


donation_food_item = db.Table(
    'donation_food_item',
    db.Column('donation_id', db.Integer, db.ForeignKey('donation.id', ondelete='CASCADE')),
    db.Column('food_item_id', db.Integer, db.ForeignKey('food_item.id', ondelete='CASCADE')),
)


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    donor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    donor = db.relationship('User', backref='donations')

    food_items = db.relationship('FoodItem', secondary=donation_food_item)

    def to_json(self):
        return {
            'id': self.id,
            'donor': self.donor.name,
            'foodItems': list(map(lambda item: item.name, self.food_items))
        }


class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }