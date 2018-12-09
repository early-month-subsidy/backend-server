# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-12-9 leo : Init

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import User, Order, Restaurant, OrderItem, OrderItemStatus, OrderStatus

order_create_parser = reqparse.RequestParser()
order_create_parser.add_argument('remark', required=False)
order_create_parser.add_argument('restaurant_id', type=int, required=True)
order_create_parser.add_argument('items', type=int, action='append', required=True)


class OrderUserAll(Resource):
    @jwt_required
    def get(self):
        current_user = User.find_by_username(get_jwt_identity())
        orders = Order.find_by_owner_id(current_user.id)
        return {
            'orders': [o.to_json() for o in orders]
        }

    @jwt_required
    def post(self):
        data = order_create_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        restaurant = Restaurant.find_by_id(data['restaurant_id'])
        order = Order(remark=data['remark'],
                      owner_id=current_user.id,
                      restaurant_id=restaurant.id,
                      total_cost=0)
        items_ids = data['items']
        items = [OrderItem.find_by_id(id) for id in items_ids]
        try:
            for item in items:
                item.status = OrderItemStatus.CONFIRMED
                item.food.sales += item.quantity
                order.items.append(item)
                order.total_cost += item.quantity * item.food.price
                db.session.add(item)
            db.session.add(order)
            db.session.commit()
            return {
                'order': order.to_json()
            }, 200
        except:
            db.session.rollback()
            return {
                'message': 'Something went wrong.',
            }, 400


class OrderUserSingle(Resource):
    @jwt_required
    def get(self, order_id):
        order = Order.find_by_id(order_id)
        return {
            'order': order.to_json()
        }, 200

    @jwt_required
    def post(self, order_id):
        data = order_create_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        order = Order.find_by_id(order_id)
        order.remark = order.remark + ' | ' + data['remark']
        if order.owner_id == current_user.id and order.status == OrderStatus.UNFILLED:
            items_ids = data['items']
            items = [OrderItem.find_by_id(id) for id in items_ids]
            try:
                for item in items:
                    item.status = OrderItemStatus.CONFIRMED
                    item.food.sales += item.quantity
                    order.items.append(item)
                    order.total_cost += item.quantity * item.food.price
                    db.session.add(item)
                db.session.add(order)
                db.session.commit()
                return {
                    'order': order.to_json()
                }, 200
            except:
                db.session.rollback()
                return {
                    'message': 'Something went wrong.'
                }, 400
        else:
            return {
                'message': 'You can not change this order.'
            }, 403

    @jwt_required
    def put(self, order_id):
        current_user = User.find_by_username(get_jwt_identity())
        order = Order.find_by_id(order_id)
        if order.owner_id == current_user.id:
            order.status = OrderStatus.UNPAID
            try:
                db.session.add(order)
                db.session.commit()
                return {
                    'message': 'Ready to pay order %s.' % order.id
                }, 200
            except:
                db.session.rollback()
                return {
                    'message': 'Something went wrong.'
                }, 400
        else:
            return {
                'message': 'You do not have the right to pay the order.'
            }, 403


class OrderSellerAll(Resource):
    @jwt_required
    def get(self, restaurant_id):
        current_user = User.find_by_username(get_jwt_identity())
        restaurant = Restaurant.find_by_id(restaurant_id)
        if restaurant.owner_id == current_user.id:
            orders = Order.find_by_restaurant_id(restaurant_id)
            return {
                'orders': [o.to_json() for o in orders]
            }, 200
        else:
            return {
                'message': 'This restaurant is not yours.'
            }, 403


class OrderSellerSingle(Resource):
    @jwt_required
    def get(self, order_id):
        current_user = User.find_by_username(get_jwt_identity())
        order = Order.find_by_id(order_id)
        if order.restaurant.owner_id == current_user.id:
            return {
                'order': order.to_json()
            }, 200
        else:
            return {
                'message': 'This restaurant is not yours.'
            }, 403

    @jwt_required
    def put(self, order_id):
        current_user = User.find_by_username(get_jwt_identity())
        order = Order.find_by_id(order_id)
        if order.restaurant.owner_id == current_user.id:
            try:
                order.status = OrderStatus.FINISHED
                db.session.add(order)
                db.session.commit()
                return {
                    'message': 'Order %s successfully paid.' % order.id
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

    @jwt_required
    def delete(self, order_id):
        current_user = User.find_by_username(get_jwt_identity())
        order = Order.find_by_id(order_id)
        if order.restaurant.owner_id == current_user.id:
            try:
                db.session.delete(order)
                db.session.commit()
                return {
                    'message': 'Order %s delete success.' % order.id
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
