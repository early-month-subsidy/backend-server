# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-11-7 leo : Init

from datetime import timedelta
from flask import url_for
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from captcha.image import ImageCaptcha
from .. import db, redis_db
from ..models import User
from ..common.utils import generate_captcha_chars

captcha_generator = ImageCaptcha()

captcha_parser = reqparse.RequestParser()
captcha_parser.add_argument('captcha_id', help='This field cannot be blank', required=True)
captcha_parser.add_argument('captcha', help='This field cannot be blank', required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help='This field cannot be blank', required=True)
login_parser.add_argument('password', help='This field cannot be blank', required=True)

registration_parser = reqparse.RequestParser()
registration_parser.add_argument('username', help='This field cannot be blank', required=True)
registration_parser.add_argument('password', help='This field cannot be blank', required=True)
registration_parser.add_argument('captcha_id', help='This field cannot be blank', required=True)
registration_parser.add_argument('captcha', help='This field cannot be blank', required=True)


class Captcha(Resource):
    def get(self):
        chars = generate_captcha_chars(len=4)
        captcha_id = generate_captcha_chars(len=10)
        filename = captcha_id + '.png'
        redis_db.set('captcha.' + captcha_id, chars.lower())
        redis_db.expire('captcha.' + captcha_id, timedelta(minutes=10))
        captcha_generator.write(chars, 'app/static/captchas/' + filename)
        return {
            'captcha_id': captcha_id,
            'url': url_for('static', filename='captchas/' + filename, _external=True)
        }

    def post(self):
        data = captcha_parser.parse_args()
        captcha_id = 'captcha.' + data['captcha_id']
        if redis_db.get(captcha_id).decode('utf-8') == data['captcha'].lower():
            return {
                'message': 'captcha is correct.'
            }, 200
        else:
            return {
                'message': 'captcha is wrong.'
            }, 403
        


class UserRegistration(Resource):
    def post(self):
        data = registration_parser.parse_args()

        captcha_id = 'captcha.' + data['captcha_id']
        if redis_db.get(captcha_id).decode('utf-8') != data['captcha'].lower():
            return {
                'message': 'captcha is wrong.'
            }, 403

        if User.find_by_username(data['username']):
            return {
                'message': 'User %s already exists.' % data['username']
            }, 403

        new_user = User(username=data['username'], password=data['password'])
        try:
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User %s was created.' % new_user.username,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201
        except:
            return {
                'message': 'Something went wrong.'
            }, 500


class UserLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return {
                'message': 'User %s does not exist.' % data['username']
            }, 403

        if current_user.verify_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as %s.' % data['username'],
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {
                'message': 'Wrong credentials.'
            }, 401


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = 'jti.' + jti
            redis_db.set(revoked_token, 'True')
            redis_db.expire(revoked_token, timedelta(hours=2))
            return {
                'message': 'Access token has been revoked.'
            }, 200
        except:
            return {
                'message': 'Something went wrong.'
            }, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = 'jti.' + jti
            redis_db.set(revoked_token, 'True')
            redis_db.expire(revoked_token, timedelta(days=1))
            return {
                       'message': 'Refresh token has been revoked.'
                   }, 200
        except:
            return {
                       'message': 'Something went wrong.'
                   }, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {
            'access_token': access_token
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
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
