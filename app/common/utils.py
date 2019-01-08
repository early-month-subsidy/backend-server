# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-11-26 leo : Init

import random
import string
import requests
import json
from flask import current_app
from datetime import timedelta
from .. import redis_db

ALLOW_EXTENSION = {'png', 'jpg', 'jpeg', 'gif'}


def generate_captcha_chars(len):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(len))


def get_wx_access_token():
    if not bool(redis_db.get('wx_access_token')):
        url = 'https://api.weixin.qq.com/cgi-bin/token?' + \
              'grant_type=client_credential&appid=' + \
              current_app.config.get('APPID') + \
              '&secret=' + current_app.config.get('APP_SECRET')
        try:
            res = requests.get(url).content.decode('utf-8')
            res_data = json.loads(res)
            wx_access_token = res_data["access_token"]
            expire_time = res_data["expires_in"]
            redis_db.set('wx_access_token', wx_access_token)
            redis_db.expire('wx_access_token', timedelta(seconds=expire_time))
        except:
            return False
    return redis_db.get('wx_access_token')
