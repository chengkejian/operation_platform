#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: __init__.py
@time: 2016/9/1 16:54
"""
from flask import Blueprint
auth = Blueprint('auth',__name__)
from . import views
