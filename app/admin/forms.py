#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: forms.py
@time: 2016/11/1 16:56
"""
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField,BooleanField
from wtforms import validators,ValidationError
from ..models import Role,User


class EditProfileFrom(FlaskForm):
	name = StringField(u'姓名',[validators.length(max=10)])
	department = StringField(u'部门',[validators.length(max=10)])
	about_me = TextAreaField(u'描述')
	submit = SubmitField(u'提交')

class EditProfileAdminForm(FlaskForm):
		username = StringField('Username',[validators.DataRequired(),validators.length(1,64),
									   validators.Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
														 'Usernames must have only letters,''numbers, dots or underscores')])
		email = StringField('Email',[validators.DataRequired(),validators.length(1,64),validators.Email()])
		confirmed = BooleanField('Confirmed')
		role = SelectField('Role', coerce=int)
		name = StringField(u'姓名',[validators.length(max=10)])
		department = StringField(u'部门',[validators.length(max=10)])
		about_me = TextAreaField(u'描述')
		submit = SubmitField(u'提交')
		def __init__(self,user,*args, **kwargs):
			super(EditProfileAdminForm, self).__init__(*args, **kwargs)
			self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
			self.user = user
		# def validate_email(self,field):
		# 	if field.data != self.user.email and \
		# 		User.query.filter_by(email=field.data).first():
		# 		raise ValidationError('Email already registered.')
		def validate_username(self,field):
			if field.data != self.user.username and \
				User.query.filter_by(email=field.data).first():
				raise ValidationError('Username already in use.')

class EditUserForm(FlaskForm):
		username = StringField('Username',[validators.DataRequired(),validators.length(1,64),
									   validators.Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
														 'Usernames must have only letters,''numbers, dots or underscores')])
		email = StringField('Email',[validators.DataRequired(),validators.length(1,64),validators.Email()])
		confirmed = BooleanField('Confirmed')
		role = SelectField('Role', coerce=int)
		name = StringField(u'姓名',[validators.length(max=10)])
		department = StringField(u'部门',[validators.length(max=10)])
		about_me = TextAreaField(u'描述')
		def __init__(self,*args, **kwargs):
			super(EditUserForm, self).__init__(*args, **kwargs)
			self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]

		# def validate_email(self,field):
		# 	if field.data != self.user.email and \
		# 		User.query.filter_by(email=field.data).first():
		# 		raise ValidationError('Email already registered.')
		# def validate_username(self,field):
		# 	if field.data != self.user.username and \
		# 		User.query.filter_by(email=field.data).first():
		# 		raise ValidationError('Username already in use.')

