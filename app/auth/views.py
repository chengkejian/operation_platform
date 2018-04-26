#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: views.py
@time: 2016/9/1 16:56
"""
from flask import render_template,current_app,redirect,session,flash,url_for,request
from flask_login import login_user,logout_user,login_required,current_user
from . import auth
from .forms  import LoginFrom,RegistrationForm,RepasswordForm,FopasswordForm,FpasswdForm
from ..models import User
from .. import db
from ..email import send_email
from ..decorators import admin_required
import datetime


@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginFrom()
	register_form = RegistrationForm()
	fopassword_form = FopasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is not None and user.verify_password(form.password.data):
			session['name'] = form.name.data
			login_user(user,form.remember_me.data)
			session['last_time'] = user.last_seen
			current_user.ping()
			return redirect(request.args.get('next') or url_for('main.index'))
		flash(u'用户名或密码错误！','danger')
	return render_template('auth/login.html',form=form,register_form=register_form,fopassword_form=fopassword_form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.','success')
	return redirect(url_for('auth.login'))

@auth.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm(request.form)
	if form.validate_on_submit():
		user = User(username=form.username.data,
					email = form.email.data,
					password = form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token_id()
		send_email(user.email,'New User','auth/email/confirm',user=user,token=token)
		flash('A confirmation email has been sent to your %s,please check.'  % user.email,'warning')
	return redirect(url_for('auth.login'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account. Thanks!','success')
	else:
		flash('The confirmation link is invalid or has expired.','warning')
	return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
	if current_user.is_authenticated \
			and not current_user.confirmed \
			and request.endpoint[:5] != 'auth.' \
			and request.endpoint != 'static':
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def	resend_confirmation():
	token = current_user.generate_confirmation_token_id()
	send_email(current_user.email,'New User','auth/email/confirm',user=current_user,token=token)
	flash('A new confirmation email has been sent to you by email.','warning')
	return redirect(url_for('main.index'))

@auth.route('/repasswd',methods=['GET','POST'])
@login_required
def repasswd():
	form = RepasswordForm()
	if form.validate_on_submit():
		password = form.password.data
		current_user.password = password
		db.session.commit()
		flash('passwd  updated successfully.','success')
		return redirect(url_for('main.index'))
	return render_template('auth/repassword.html',form=form)

@auth.route('/fopasswd',methods=['GET','POST'])
def fopasswd():
	form = FopasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			flash('The user does not exist;','danger')
			return redirect(url_for('auth.login'))
		else:
			token = user.generate_confirmation_token_id()
			send_email(user.email,'Reset PASSWD','auth/email/repassword',user=user,token=token)
			flash('View your registered email , click on the links in the email to reset the password.','warning')
			return redirect(url_for('auth.login'))
	return redirect(url_for('auth.login'))

@auth.route('/fpasswd/<token>/<user>',methods=['GET','POST'])
def fpasswd(token,user):
	form = FpasswdForm()
	user = User.query.filter_by(username=user).first()
	if form.validate_on_submit():
		password = form.password.data
		user.password=password
		db.session.commit()
		flash('passwd  reset successfully.','success')
		return redirect(url_for('auth.login'))
	return render_template('auth/fpasswd.html',form=form)








