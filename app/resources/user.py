# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-11-7 leo : Init

from flask_restful import Resource, reqparse
from .. import db
from ..models import User

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if User.find_by_username(data['username']):
            return {
                'message': 'User %s already exists.' % data['username']
            }, 403

        new_user = User(username=data['username'], password=data['password'])
        try:
            db.session.add(new_user)
            db.session.commit()
            return {
                'message': 'User %s was created.' % new_user.username
            }, 201
        except:
            return {
                'message': 'Something went wrong.'
            }, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return {
                'message': 'User %s does not exist.' % data['username']
            }, 403

        if current_user.verify_password(data['password']):
            return {
                'message': 'Logged in as %s.' % data['username']
            }, 200
        else:
            return {
                'message': 'Wrong credentials.'
            }, 401


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
        users = User.query.all()
        return {
            'users': [{
                'username': x.username,
                'password': x.password_hash
            } for x in users],
        }, 200

    def delete(self):
        try:
            num_rows_delete = db.session.query(User).delete()
            db.session.commit()
            return {
                'message': '%s row(s) deleted.' % num_rows_delete
            }, 200
        except:
            return {
                'message': 'Something went wrong.'
            }, 500


class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }
