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
    nickname = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    restaurants = db.relationship('Restaurant', backref='owner')
    orders = db.relationship('Order', backref='owner')

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
    foods = db.relationship('Food', cascade='all,delete', backref='category')

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
            'restaurant_id': self.restaurant_id,
            'foods': [f.to_json() for f in self.foods]
        }


class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(64))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(128))
    likes = db.Column(db.Integer, default=0)
    sales = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    @classmethod
    def find_by_category_id(cls, category_id):
        return cls.query.filter_by(category_id=category_id).order_by(cls.likes).all()

    @classmethod
    def find_by_id(cls, food_id):
        return cls.query.get(food_id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image': self.image,
            'likes': self.likes,
            'sales': self.sales,
            'category_id': self.category_id
        }


class OrderItemStatus(object):
    ORDERING = 'ORDERING'
    CONFIRMED = 'CONFIRMED'
    CANCELED = 'CANCELED'


class OrderItem(TimestampMixin, db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(16), default=OrderItemStatus.ORDERING)
    quantity = db.Column(db.Integer, default=1)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    owner = db.relationship('User')
    food = db.relationship('Food')

    @classmethod
    def find_by_board_id(cls, board_id):
        return cls.query.filter_by(board_id=board_id, status=OrderItemStatus.ORDERING).all()

    @classmethod
    def find_by_id(cls, order_item_id):
        return cls.query.get(order_item_id)

    def to_json(self):
        return {
            'id': self.id,
            'status': self.status,
            'quantity': self.quantity,
            'owner': {
                'id': self.owner_id,
                'name': self.owner.username
            },
            'board_id': self.board_id,
            'food': {
                'id': self.food_id,
                'name': self.food.name
            }
        }


class OrderStatus(object):
    UNFILLED = 'UNFILLED'
    UNPAID = 'UNPAID'
    FINISHED = 'FINISHED'


class Order(TimestampMixin, db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(16), default=OrderStatus.UNFILLED)
    remark = db.Column(db.String(64))
    total_cost = db.Column(db.Float, default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = db.relationship('Restaurant')
    items = db.relationship('OrderItem', cascade='all,delete', backref='order')

    @classmethod
    def find_by_owner_id(cls, owner_id):
        return cls.query.filter_by(owner_id=owner_id).order_by(cls.updated_at).all()

    @classmethod
    def find_by_restaurant_id(cls, restaurant_id):
        return cls.query.filter_by(restaurant_id=restaurant_id).order_by(cls.created_at).all()

    @classmethod
    def find_by_id(cls, order_id):
        return cls.query.get(order_id)

    def to_json(self):
        return {
            'id': self.id,
            'created_time': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_time': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'remark': self.remark,
            'total_cost': self.total_cost,
            'owner_id': self.owner_id,
            'restaurant': {
                'id': self.restaurant_id,
                'name': self.restaurant.name
            },
            'items': [i.to_json() for i in self.items]
        }
