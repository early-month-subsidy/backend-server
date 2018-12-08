# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-12-8 leo : Init

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Category, User, Restaurant

category_create_parser = reqparse.RequestParser()
category_create_parser.add_argument('name', help='This field cannot be blank', required=True)
category_create_parser.add_argument('priority', type=int, required=False)


class CategorySellerAll(Resource):
    def get(self, restaurant_id):
        categories = Category.find_by_restaurant_id(restaurant_id)
        return {
            'categories': [c.to_json() for c in categories]
        }, 200

    @jwt_required
    def post(self, restaurant_id):
        data = category_create_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        restaurant = Restaurant.find_by_id(restaurant_id)
        if restaurant.owner_id == current_user.id:
            category = Category(name=data['name'], priority=data['priority'], restaurant_id=restaurant_id)
            restaurant.categories.append(category)
            try:
                db.session.add(restaurant)
                db.session.add(category)
                db.session.commit()
                return {
                    'category': category.to_json()
                }, 200
            except:
                db.session.rollback()
                return {
                    'message': 'Something went wrong.'
                }, 400
        else:
            return {
                'message': 'This restaurant is not yours.'
            }, 403


class CategorySingle(Resource):
    def get(self, restaurant_id, category_id):
        category = Category.find_by_id(category_id)
        return {
            'category': category.to_json()
        }, 200

    @jwt_required
    def put(self, restaurant_id, category_id):
        current_user = User.find_by_username(get_jwt_identity())
        restaurant = Restaurant.find_by_id(restaurant_id)
        category = Category.find_by_id(category_id)
        # TODO: change category priority
        if restaurant.owner_id == current_user.id:
            return {
                'message': 'Change category %s priority success.' % category.name
            }
        else:
            return {
                'message': 'This restaurant is not yours.'
            }, 403

    @jwt_required
    def delete(self, restaurant_id, category_id):
        current_user = User.find_by_username(get_jwt_identity())
        restaurant = Restaurant.find_by_id(restaurant_id)
        category = Category.find_by_id(category_id)
        if restaurant.owner_id == current_user.id:
            try:
                db.session.delete(category)
                db.session.commit()
                return {
                    'message': 'Delete category %s success.' % category.name
                }, 200
            except:
                return {
                    'message': 'Something went wrong.'
                }, 400
        else:
            return {
                'message': 'This restaurant is not yours.'
            }, 403
