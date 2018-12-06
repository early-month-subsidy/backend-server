# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-11-7 leo : Init

from flask import Blueprint
from flask_restful import Api

from . import user as user_resources
from . import restaurant as restaurant_resources

api_bp = Blueprint('api', __name__)

api = Api(api_bp)

# user routes
api.add_resource(user_resources.Captcha, '/captcha')
api.add_resource(user_resources.UserRegistration, '/registration')
api.add_resource(user_resources.UserLogin, '/login')
api.add_resource(user_resources.UserLogoutAccess, '/logout/access')
api.add_resource(user_resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user_resources.TokenRefresh, '/token/refresh')
api.add_resource(user_resources.AllUser, '/users')
api.add_resource(user_resources.SecretResource, '/secret')

# restaurant routes
api.add_resource(restaurant_resources.RestaurantSellerAll, '/seller/restaurants')
api.add_resource(restaurant_resources.RestaurantSellerSingle, '/seller/restaurant/<int:restaurant_id>')
api.add_resource(restaurant_resources.RestaurantUserAll, '/api/restaurants')
api.add_resource(restaurant_resources.RestaurantUserQuery, '/api/restaurants/query')
api.add_resource(restaurant_resources.RestaurantUploadImage, '/restaurant/<int:restaurant_id>/images')
api.add_resource(restaurant_resources.RestaurantImageSingle, '/restaurant/<int:restaurant_id>/images/<int:image_id>')
