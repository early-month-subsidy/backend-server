# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-12-8 leo : Init

from flask import url_for
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
from .. import db
from ..models import Food, User, Category
from ..common.utils import generate_captcha_chars, ALLOW_EXTENSION

food_create_parser = reqparse.RequestParser()
food_create_parser.add_argument('name', help='This field cannot be blank', required=True)
food_create_parser.add_argument('description', required=False)
food_create_parser.add_argument('price', type=float, required=True)

food_image_parser = reqparse.RequestParser()
food_image_parser.add_argument('file', type=FileStorage, location='files', required=True)


class FoodSellerAll(Resource):
    def get(self, category_id):
        foods = Food.find_by_category_id(category_id)
        return {
            'foods': [f.to_json() for f in foods]
        }, 200

    @jwt_required
    def post(self, category_id):
        data = food_create_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        category = Category.find_by_id(category_id)
        food = Food(name=data['name'], description=data['description'],
                    price=data['price'], category_id=category_id)
        category.foods.append(food)
        try:
            db.session.add(food)
            db.session.add(category)
            db.session.commit()
            return {
                'food': food.to_json()
            }, 200
        except:
            db.session.rollback()
            return {
                'message': 'Something went wrong.'
            }, 400


# TODO: add likes link.
class FoodSingle(Resource):
    def get(self, category_id, food_id):
        food = Food.find_by_id(food_id)
        return {
            'food': food.to_json()
        }, 200

    @jwt_required
    def post(self, category_id, food_id):
        data = food_image_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        food = Food.find_by_id(food_id)
        # saving photo
        photo = data['file']
        # check file type
        file_type = photo.filename.rsplit('.', 1)[1].lower()
        if file_type in ALLOW_EXTENSION:
            filename = generate_captcha_chars(16) + '.' + file_type
            photo.save('app/static/images/' + filename)
            url = url_for('static', filename='images/' + filename,
                          _external=True)
            food.image = url
            try:
                db.session.add(food)
                db.session.commit()
                return {
                           'food': food.to_json()
                       }, 200
            except:
                return {
                           'message': 'Something went wrong.'
                       }, 400
        else:
            return {
                       'message': 'Not support file type.'
                   }, 403

    @jwt_required
    def delete(self, category_id, food_id):
        current_user = User.find_by_username(get_jwt_identity())
        food = Food.find_by_id(food_id)
        try:
            db.session.delete(food)
            db.session.commit()
            return {
                       'message': 'Delete food %s success.' % food.name
                   }, 200
        except:
            return {
                       'message': 'Something went wrong.'
                   }, 400
