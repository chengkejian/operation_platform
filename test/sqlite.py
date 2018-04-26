#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: sqlite.py
@time: 2016/8/22 16:27
"""
import sqlite3

# cx = sqlite3.connect("E:/Projects/flasky/test/test.sqlite")
cx = sqlite3.connect("E:/Projects/flasky/data-dev.sqlite")
cu=cx.cursor()
print cu.execute("select name from sqlite_master  order by name").fetchall()
print cu.execute("select  * from roles").fetchall()