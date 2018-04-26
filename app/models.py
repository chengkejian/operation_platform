#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: models.py
@time: 2016/8/30 16:04
"""
from . import db
from  werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from . import login_manager
from flask import current_app,session,request
from  itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime,hashlib
from markdown import markdown
import bleach

class Permission():
	ANDROID = 0x01
	ANDROIDSTEP = 0x02
	IOS = 0x04
	IOSSTEP = 0x08
	CONSOLE = 0x10
	CONSOLESTEP = 0x20
	ADMINISTER = 0x80

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	default = db.Column(db.Boolean,default=False,index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role')
	def __repr__(self):
		return 'Role %r' % self.name
	@staticmethod
	def insert_roles():
		roles = {
			'Mobimer':(Permission.ANDROIDSTEP |
					Permission.IOSSTEP |
					Permission.CONSOLESTEP,True),
			'Android':(Permission.ANDROID |
					   Permission.ANDROIDSTEP,False),
			'Ios':(Permission.IOS |
				   Permission.IOSSTEP,False),
			'Console':(Permission.CONSOLE |
					   Permission.CONSOLESTEP,False),
			'Administrator':(0xff,False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()

class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64),index=True)
	name = db.Column(db.String(64))
	department = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	member_since = db.Column(db.DateTime(),default=datetime.datetime.now())
	last_seen = db.Column(db.DateTime(),default=datetime.datetime.now())
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean,default=False)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	posts = db.relationship('Post',backref='author',lazy='dynamic')
	def __init__(self,**kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email == current_app.config['MOBIM_ADMIN']:
				self.role = Role.query.filter_by(permissions=0xff).first()
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()
	def __repr__(self):
		return '<User %r>' % self.username

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

	def	generate_confirmation_token_id(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'],expiration)
		return s.dumps({'confirm':self.id})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	def can(self,permissions):
		return self.role is not None and (self.role.permissions & permissions) == permissions
	def is_admin(self):
		return self.can(Permission.ADMINISTER)

	def ping(self):
		self.last_seen = datetime.datetime.now()
		db.session.add(self)

	def gravatar(self,size=100,default='identicon',rating='g'):
		if request.is_secure:
			url = 'https://secure.gravatar.com/avatar'
		else:
			url = 'http://www.gravatar.com/avatar'
		hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url,hash=hash,size=size,default=default,rating=rating)



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer,primary_key=True)
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	timestamp = db.Column(db.DateTime,index=True,default=datetime.datetime.now())
	author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

	@staticmethod
	def on_changed_body(target,value,oldvalue,initiator):
		allowwd_tag = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
						'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
						'h1', 'h2', 'h3', 'p']
		target.body_html = bleach.linkify(bleach.clean(
				markdown(value,output_format='html'),tags=allowwd_tag,strip=True))
db.event.listen(Post.body, 'set', Post.on_changed_body)

class AndroidChannel(db.Model):
	__tablename__ = 'android_channel_info'
	id = db.Column(db.Integer,primary_key=True)
	channel_name = db.Column(db.Text)
	channel = db.Column(db.Integer,index=True)
	app_name = db.Column(db.Text)
	package_link = db.Column(db.String(64))
	need_replace_ico = db.Column(db.Boolean,default=False)
	version = db.Column(db.String(64))
	platform = db.Column(db.String(128))
	package_status = db.Column(db.SmallInteger)
	package_upload_status = db.Column(db.SmallInteger)
	package_time = db.Column(db.String(64))
	package_name = db.Column(db.String(64))

class AndroidPlatform(db.Model):
	__tablename__ = 'android_platform'
	id = db.Column(db.Integer,primary_key=True)
	platform = db.Column(db.String(128))
	platform_name = db.Column(db.Text)
	assemble_name = db.Column(db.String(64))

