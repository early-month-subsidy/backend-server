# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-10-13 leo : Init

from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return "<h1>Early Month Subsidy ordering system.</h1>"
