# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-12-9 leo : Init

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import OrderItem, User, Board

order_item_create_parser = reqparse.RequestParser()
order_item_create_parser.add_argument('quantity', type=int, help='This field cannot be blank', required=True)
order_item_create_parser.add_argument('food_id', type=int, help='This field cannot be blank', required=True)

order_item_update_parser = reqparse.RequestParser()
order_item_update_parser.add_argument('quantity', type=int, required=False)
order_item_update_parser.add_argument('action', required=False)


class OrderItemAll(Resource):
    def get(self, board_id):
        order_items = OrderItem.find_by_board_id(board_id)
        return {
            'order_items': [i.to_json() for i in order_items]
        }, 200

    @jwt_required
    def post(self, board_id):
        data = order_item_create_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        board = Board.find_by_id(board_id)
        board.occupation = True
        order_item = OrderItem(quantity=data['quantity'],
                               owner_id=current_user.id,
                               board_id=board_id,
                               food_id=data['food_id'])
        try:
            db.session.add(order_item)
            db.session.add(board)
            db.session.commit()
            return {
                'order_item': order_item.to_json()
            }, 200
        except:
            db.session.rollback()
            return {
                'message': 'Something went wrong.'
            }, 500


# TODO: cancel order item by seller
class OrderItemSingle(Resource):
    def get(self, order_item_id):
        order_item = OrderItem.find_by_id(order_item_id)
        return {
            'order_item': order_item.to_json()
        }, 200

    @jwt_required
    def put(self, order_item_id):
        # TODO: add status judge
        data = order_item_update_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        order_item = OrderItem.find_by_id(order_item_id)
        if order_item.owner_id == current_user.id:
            action = data['action']
            if action == 'increment':
                order_item.quantity += 1
            elif action == 'decrement':
                order_item.quantity -= 1
            elif data['quantity']:
                    order_item.quantity = data['quantity']
            else:
                return {
                    'message': 'Unknown action.'
                }, 403
            try:
                db.session.add(order_item)
                db.session.commit()
                return {
                    'order_item': order_item.to_json()
                }, 200
            except:
                db.session.rollback()
                return {
                    'message': 'Something went wrong.'
                }, 500
        else:
            return {
                'message': 'This order item is not yours.'
            }, 403

    @jwt_required
    def delete(self, order_item_id):
        current_user = User.find_by_username(get_jwt_identity())
        order_item = OrderItem.find_by_id(order_item_id)
        if order_item.owner_id == current_user.id:
            try:
                db.session.delete(order_item)
                db.session.commit()
                return {
                    'message': 'Order item %s delete success.' % order_item_id
                }, 200
            except:
                db.session.rollback()
                return {
                    'message': 'Something went wrong.'
                }, 500
        else:
            return {
                'message': 'This order item is not yours.'
            }, 403
