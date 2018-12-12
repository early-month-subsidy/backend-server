# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-12-3 leo : Init

from flask import url_for
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
from .. import db
from ..models import User, Restaurant, RestaurantImage
from ..common.utils import generate_captcha_chars, ALLOW_EXTENSION

restaurant_create_parser = reqparse.RequestParser()
restaurant_create_parser.add_argument('name', help='This field cannot be blank', required=True)
restaurant_create_parser.add_argument('introduction', required=False)
restaurant_create_parser.add_argument('opening_time', required=False)
restaurant_create_parser.add_argument('address', required=False)

restaurant_update_parser = reqparse.RequestParser()
restaurant_update_parser.add_argument('introduction', required=False)
restaurant_update_parser.add_argument('opening_time', required=False)
restaurant_update_parser.add_argument('address', required=False)

restaurant_query_parser = reqparse.RequestParser()
restaurant_query_parser.add_argument('name', location='args')

restaurant_image_parser = reqparse.RequestParser()
restaurant_image_parser.add_argument('file', type=FileStorage, location='files', required=True)

restaurant_image_moving_parser = reqparse.RequestParser()
restaurant_image_moving_parser.add_argument('direction')


class RestaurantSellerAll(Resource):
    @jwt_required
    def get(self):
        current_user = User.find_by_username(get_jwt_identity())
        restaurants = Restaurant.find_by_userid(current_user.id)
        return {
            'restaurants': [r.to_json() for r in restaurants]
        }, 200

    @jwt_required
    def post(self):
        data = restaurant_create_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        new_restaurant = Restaurant(name=data['name'],
                                    introduction=data['introduction'],
                                    opening_time=data['opening_time'],
                                    address=data['address'],
                                    owner_id=current_user.id)
        try:
            db.session.add(new_restaurant)
            db.session.commit()
            return {
                'restaurant': new_restaurant.to_json()
            }, 200
        except:
            db.session.rollback()
            return {
                'message': 'Something went wrong.',
            }, 500


class RestaurantSellerSingle(Resource):
    @jwt_required
    def get(self, restaurant_id):
        restaurant = Restaurant.find_by_id(restaurant_id)
        current_user = User.find_by_username(get_jwt_identity())
        if restaurant.owner_id == current_user.id:
            return {
                'restaurant': restaurant.to_json()
            }, 200
        else:
            return {
                'message': 'This restaurant is not yours.'
            }, 403

    @jwt_required
    def put(self, restaurant_id):
        data = restaurant_update_parser.parse_args()
        restaurant = Restaurant.find_by_id(int(restaurant_id))
        current_user = User.find_by_username(get_jwt_identity())
        if restaurant.owner_id == current_user.id:
            restaurant.introduction = data['introduction']
            restaurant.opening_time = data['opening_time']
            restaurant.address = data['address']
            try:
                db.session.add(restaurant)
                db.session.commit()
                return {
                    'restaurant': restaurant.to_json()
                }, 200
            except:
                db.session.rollback()
                return {
                    'message': 'Something went wrong.'
                }, 500
        else:
            return {
                'message': 'This restaurant is not yours.'
            }, 403

    @jwt_required
    def delete(self, restaurant_id):
        restaurant = Restaurant.find_by_id(restaurant_id)
        current_user = User.find_by_username(get_jwt_identity())
        if restaurant.owner_id == current_user.id:
            try:
                db.session.delete(restaurant)
                db.session.commit()
                return {
                    'message': 'Restaurant %s delete success.' % restaurant.name
                }, 200
            except:
                db.session.rollback()
                return {
                    'message': 'Something went wrong.'
                }, 500
        else:
            return {
                'message': 'This restaurant is not yours.'
            }, 403


class RestaurantUserAll(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return {
            'restaurants': [r.to_json() for r in restaurants]
        }, 200


class RestaurantUserQuery(Resource):
    def get(self):
        data = restaurant_query_parser.parse_args()
        restaurants = Restaurant.query.filter(Restaurant.name.like('%%s%', data['name'])).all()
        return {
            'restaurants': [r.to_json() for r in restaurants]
        }, 200


class RestaurantUserSingle(Resource):
    def get(self, restaurant_id):
        restaurant = Restaurant.find_by_id(restaurant_id)
        return {
            'restaurant': restaurant.to_json()
        }, 200


class RestaurantUploadImage(Resource):
    @jwt_required
    def post(self, restaurant_id):
        data = restaurant_image_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        restaurant = Restaurant.find_by_id(restaurant_id)
        # check operation authorization
        if restaurant.owner_id == current_user.id:
            photo = data['file']
            # check file type
            file_type = photo.filename.rsplit('.', 1)[1].lower()
            if file_type in ALLOW_EXTENSION:
                filename = generate_captcha_chars(16) + '.' + file_type
                photo.save('app/static/images/' + filename)
                url = url_for('static', filename='images/' + filename, _external=True)
                order_id = RestaurantImage.restaurant_image_count(restaurant_id)
                new_image = RestaurantImage(order_id=order_id,
                                            image_url=url,
                                            restaurant_id=restaurant_id)
                try:
                    db.session.add(new_image)
                    db.session.commit()
                    return {
                        'image': new_image.to_json()
                    }, 200
                except:
                    db.session.rollback()
                    return {
                        'message': 'Something went wrong.'
                    }, 500
            else:
                return {
                    'message': 'Not support file type.'
                }, 403
        else:
            return {
                'message': 'This restaurant is not yours.'
            }, 403


class RestaurantImageSingle(Resource):
    @jwt_required
    def get(self, restaurant_id, image_id):
        image = RestaurantImage.find_by_id(image_id)
        return {
            'image': image.to_json()
        }, 200

# TODO: picture moving
#     @jwt_required
#     def pache(self, restaurant_id, image_id):

    @jwt_required
    def delete(self, restaurant_id, image_id):
        image = RestaurantImage.find_by_id(image_id)
        try:
            # TODO: order fix
            db.session.delete(image)
            db.session.commit()
            return {
                'message': 'Restaurant image %s delete success.' % image_id
            }, 200
        except:
            db.session.rollback()
            return {
                'message': 'Something went wrong.'
            }, 500

