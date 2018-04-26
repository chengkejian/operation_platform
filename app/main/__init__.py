#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: __init__.py
@time: 2016/8/23 14:39
"""
from flask import Blueprint


main = Blueprint('main',__name__)

from . import views,errors