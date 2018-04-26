#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: manage.py
@time: 2016/8/30 16:32
"""
import os
from app import create_app,db
from app.models import User,Role
from flask_migrate import Migrate,MigrateCommand
from flask_script import Shell,Manager

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
	# manager.run()
	app.run(host='0.0.0.0')






