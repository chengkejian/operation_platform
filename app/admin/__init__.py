#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: __init__.py.py
@time: 2016/11/1 16:54
"""
from flask import Blueprint
admin = Blueprint('admin',__name__)
from . import views
