#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: forms.py
@time: 2016/9/5 15:48
"""
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms import validators,ValidationError
from ..models import User

class LoginFrom(FlaskForm):
	name = StringField('NAME:',[validators.DataRequired(), validators.length(max=64)])
	password = PasswordField('PASSWORD:',[validators.DataRequired()])
	remember_me = BooleanField(u'记住我')
	submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
	username = StringField('Username',[validators.DataRequired(),validators.length(1,64),
									   validators.Regexp('^[A-Za-z][A-Za-z0-9_]*$',0,
														 'Usernames must have only letters,''numbers, dots or underscores')])
	email = StringField('Email',[validators.DataRequired(),validators.length(1,64),validators.Email()])
	password = PasswordField('Password',[validators.DataRequired(),validators.EqualTo('password2',message='Passwords must match.')])
	password2 = PasswordField('Confirm password',[validators.DataRequired()])

	def validate_username(self,filed):
		if User.query.filter_by(username=filed.data).first():
			raise ValidationError('Username already in use.')
	# def validate_email(self,filed):
	# 	if User.query.filter_by(email=filed.data).first():
	# 		raise ValidationError('Email already registered.')

class RepasswordForm(FlaskForm):
	old_password = PasswordField('Old Password',[validators.DataRequired()])
	password = PasswordField('New Password',[validators.DataRequired(),validators.EqualTo('password2',message='Passwords must match.')])
	password2 = PasswordField('Confirm password',[validators.DataRequired()])
	submit = SubmitField('Register')

class FopasswordForm(FlaskForm):
	name = StringField(u'登录名：',[validators.DataRequired(), validators.length(max=64)])

class FpasswdForm(FlaskForm):
	password = PasswordField('New Password',[validators.DataRequired(),validators.EqualTo('password2',message='Passwords must match.')])
	password2 = PasswordField('Confirm password',[validators.DataRequired()])
	submit = SubmitField('Register')

