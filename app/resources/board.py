# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-12-6 leo : Init

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_
from .. import db
from ..models import Board, User, Restaurant, OrderItem, OrderItemStatus

board_create_parser = reqparse.RequestParser()
board_create_parser.add_argument('name', help='This field cannot be blank', required=True)
board_create_parser.add_argument('seat_num', type=int, required=False)

board_lock_parser = reqparse.RequestParser()
board_lock_parser.add_argument('action', help='This field cannot be blank', required=True)


class BoardSellerAll(Resource):
    def get(self, restaurant_id):
        boards = Board.find_by_restaurant_id(restaurant_id)
        return {
            'boards': [b.to_json() for b in boards]
        }, 200

    @jwt_required
    def post(self, restaurant_id):
        data = board_create_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        restaurant = Restaurant.find_by_id(restaurant_id)
        if restaurant.owner_id == current_user.id:
            # TODO create qr code (not sure format)
            board = Board(name=data['name'], seat_num=data['seat_num'], restaurant_id=restaurant_id)
            restaurant.boards.append(board)
            try:
                db.session.add(restaurant)
                db.session.add(board)
                db.session.commit()
                return {
                    'board': board.to_json()
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


class BoardSingle(Resource):
    def get(self, restaurant_id, board_id):
        board = Board.find_by_id(board_id)
        return {
            'board': board.to_json()
        }, 200

    @jwt_required
    def put(self, restaurant_id, board_id):
        data = board_lock_parser.parse_args()
        current_user = User.find_by_username(get_jwt_identity())
        restaurant = Restaurant.find_by_id(restaurant_id)
        board = Board.find_by_id(board_id)
        if restaurant.owner_id == current_user.id:
            action = data['action'].lower()
            message = 'Restaurant %s Board %s ' % (restaurant.name, board.name)
            if action == 'lock':
                board.occupation = True
                message = message + 'lock success.'
            elif action == 'unlock':
                board.occupation = False
                message = message + 'unlock success.'
                # delete all ordering order item.
                db.session.query(OrderItem).filter(
                    and_(OrderItem.status == OrderItemStatus.ORDERING,
                         OrderItem.board_id == board_id)).delete()
            else:
                return {
                    'message': 'Unknown action.'
                }, 403
            try:
                db.session.add(board)
                db.session.commit()
                return {
                    'message': message
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
    def delete(self, restaurant_id, board_id):
        current_user = User.find_by_username(get_jwt_identity())
        restaurant = Restaurant.find_by_id(restaurant_id)
        board = Board.find_by_id(board_id)
        if restaurant.owner_id == current_user.id:
            try:
                db.session.delete(board)
                db.session.commit()
                return {
                    'message': 'Delete board %s success.' % board.name
                }, 200
            except:
                return {
                    'message': 'Something went wrong.'
                }, 400
        else:
            return {
                'message': 'This restaurant is not yours.'
            }, 403
