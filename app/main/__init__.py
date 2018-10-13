# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-10-13 leo : Init

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
