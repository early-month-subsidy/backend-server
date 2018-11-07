# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-11-7 leo : Init

from flask import Blueprint
from flask_restful import Api

from . import user as user_resources

api_bp = Blueprint('api', __name__)

api = Api(api_bp)

# user routes
api.add_resource(user_resources.UserRegistration, '/registration')
api.add_resource(user_resources.UserLogin, '/login')
api.add_resource(user_resources.UserLogoutAccess, '/logout/access')
api.add_resource(user_resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user_resources.TokenRefresh, '/token/refresh')
api.add_resource(user_resources.AllUser, '/users')
api.add_resource(user_resources.SecretResource, '/secret')
