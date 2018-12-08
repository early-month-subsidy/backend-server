# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-11-26 leo : Init

import random
import string

ALLOW_EXTENSION = {'png', 'jpg', 'jpeg', 'gif'}

def generate_captcha_chars(len):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(len))
