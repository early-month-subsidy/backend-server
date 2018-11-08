# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-11-7 leo : Init

from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        return {
            'message': 'User registration',
            'data': data
        }


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        return {
            'message': 'User login',
            'data': data
        }


class UserLogoutAccess(Resource):
    def post(self):
        return {
            'message': 'User logout access'
        }


class UserLogoutRefresh(Resource):
    def post(self):
        return {
            'message': 'User logout refresh'
        }


class TokenRefresh(Resource):
    def post(self):
        return {
            'message': 'Token refresh'
        }


class AllUser(Resource):
    def get(self):
        return {
            'message': 'List of users'
        }

    def delete(self):
        return {
            'message': 'Delete all users'
        }


class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }
