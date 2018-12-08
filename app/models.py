# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-10-29 leo : Init

import json
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from . import db


class TimestampMixin(object):
    """
        Timestamp mixin
    """
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    restaurants = db.relationship('Restaurant', backref='owner')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = sha256.hash(password)

    def verify_password(self, password):
        return sha256.verify(password, self.password_hash)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def __repr__(self):
        return '<User %r>' % self.username


class Restaurant(db.Model, TimestampMixin):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    introduction = db.Column(db.String(256))
    opening_time = db.Column(db.String(64))
    address = db.Column(db.String(128))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    images = db.relationship('RestaurantImage', cascade='all,delete', backref='restaurant')
    boards = db.relationship('Board', cascade='all,delete', backref='restaurant')
    categories = db.relationship('Category', cascade='all,delete', backref='restaurant')

    @classmethod
    def find_by_userid(cls, userid):
        return cls.query.filter_by(owner_id=userid).all()

    @classmethod
    def find_by_id(cls, restaurant_id):
        return cls.query.get(restaurant_id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'introduction': self.introduction,
            'opening_time': self.opening_time,
            'address': self.address,
            'images': [image.to_json() for image in self.images],
            'boards': [b.to_json() for b in self.boards],
            'categories': [c.to_json() for c in self.categories]
        }

    def __repr__(self):
        return '<Restaurant %r>' % self.name


class RestaurantImage(db.Model):
    __tablename__ = 'restaurant_images'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, default=0, nullable=False)
    image_url = db.Column(db.String(128), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    @classmethod
    def restaurant_image_count(cls, restaurant_id):
        return cls.query.filter_by(restaurant_id=restaurant_id).count()

    @classmethod
    def find_by_id(cls, image_id):
        return cls.query.get(image_id)

    @classmethod
    def find_by_restaurant_id(cls, restaurant_id):
        return cls.query.filter_by(restaurant_id=restaurant_id).order_by(cls.order_id).all()

    def to_json(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'image_url': self.image_url,
            'restaurant_id': self.restaurant_id
        }


class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    occupation = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64), nullable=False)
    seat_num = db.Column(db.Integer, default=2)
    qr_code = db.Column(db.String(128))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    @classmethod
    def find_by_id(cls, board_id):
        return cls.query.get(board_id)

    @classmethod
    def find_by_restaurant_id(cls, restaurant_id):
        return cls.query.filter_by(restaurant_id=restaurant_id).order_by(cls.seat_num).all()

    def to_json(self):
        return {
            'id': self.id,
            'occupation': self.occupation,
            'name': self.name,
            'seat_num': self.seat_num,
            'qr_code': self.qr_code,
            'restaurant_id': self.restaurant_id
        }


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    priority = db.Column(db.Integer, default=0, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    @classmethod
    def find_by_restaurant_id(cls, restaurant_id):
        return cls.query.filter_by(restaurant_id=restaurant_id).order_by(cls.priority).all()

    @classmethod
    def find_by_id(cls, category_id):
        return cls.query.get(category_id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'priority': self.priority,
            'restaurant_id': self.restaurant_id
        }
