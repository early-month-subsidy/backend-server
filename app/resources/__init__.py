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
from . import board as board_resources
from . import category as category_resources
from . import food as food_resources
from . import order_item as order_item_resources
from . import order as order_resources

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
api.add_resource(restaurant_resources.RestaurantSellerSingle, '/seller/restaurants/<int:restaurant_id>')
api.add_resource(restaurant_resources.RestaurantUserAll, '/api/restaurants')
api.add_resource(restaurant_resources.RestaurantUserQuery, '/api/restaurants/query')
api.add_resource(restaurant_resources.RestaurantUploadImage, '/seller/restaurants/<int:restaurant_id>/images')
api.add_resource(restaurant_resources.RestaurantImageSingle, '/seller/restaurants/<int:restaurant_id>/images/<int:image_id>')

# board routes
api.add_resource(board_resources.BoardSellerAll, '/seller/restaurants/<int:restaurant_id>/boards')
api.add_resource(board_resources.BoardSingle, '/api/restaurants/<int:restaurant_id>/boards/<int:board_id>')

# category routes
api.add_resource(category_resources.CategorySellerAll, '/seller/restaurants/<int:restaurant_id>/categories')
api.add_resource(category_resources.CategorySingle, '/api/restaurants/<int:restaurant_id>/categories/<int:category_id>')

# food routes
api.add_resource(food_resources.FoodSellerAll, '/seller/categories/<int:category_id>/foods')
api.add_resource(food_resources.FoodSingle, '/api/categories/<int:category_id>/foods/<int:food_id>')

# order item routes
api.add_resource(order_item_resources.OrderItemAll, '/api/boards/<int:board_id>/order_items')
api.add_resource(order_item_resources.OrderItemSingle, '/api/order_items/<int:order_item_id>')

# order routes
api.add_resource(order_resources.OrderSellerAll, '/seller/restaurants/<int:restaurant_id>/orders')
api.add_resource(order_resources.OrderSellerSingle, '/seller/orders/<int:order_id>')
api.add_resource(order_resources.OrderUserAll, '/api/orders')
api.add_resource(order_resources.OrderUserSingle, '/api/orders/<int:order_id>')
