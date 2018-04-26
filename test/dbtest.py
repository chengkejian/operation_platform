#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: test.py
@time: 2016/8/18 17:05
"""
import os
import MySQLdb
from flask import Flask
from  flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Shell,Manager
from flask_login import UserMixin
basdir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basdir,'data-dev.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:centos@10.10.10.103/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
manager = Manager(app)
def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	users = db.relationship('User', backref='role')
	def __repr__(self):
		return 'Role %r' % self.name
class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64),index=True)
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean,default=False)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	def __repr__(self):
		return '<User %r>' % self.username



# db.create_all()
# admin_role = Role(name='Admin')
# mod_role = Role(name='Moderator')
# user_role = Role(name='User')
# # user_john = User(username='john', role=admin_role)
# # user_david = User(username='david', role=user_role)
# # user_susan = User(username='susan', role=user_role)
# db.session.add_all([admin_role, mod_role, user_role])
# db.session.commit()

if __name__ == '__main__':
	manager.run()
	# print(User.query.all())

