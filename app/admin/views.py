#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: views.py
@time: 2016/11/1 16:55
"""
from flask import render_template,redirect,flash,url_for,abort,jsonify,request,current_app
from flask_login import login_required,current_user
from . import admin
from .forms  import EditProfileFrom,EditProfileAdminForm,EditUserForm
from ..models import User,Role,Post
from .. import db
from ..decorators import admin_required
import datetime
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

@admin.route('/user/<username>',methods=['GET', 'POST'])
@login_required
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	page = request.args.get('page', 1, type=int)
	pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
			page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
			error_out=False)
	posts = pagination.items
	return render_template('/admin/user.html',user=user,posts=posts,pagination=pagination)

@admin.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileFrom()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.department = form.department.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user)
		flash(u'更新成功','success')
		return redirect(url_for('.user',username=current_user.username))
	form.name.data = current_user.name
	form.department.data = current_user.department
	form.about_me.data = current_user.about_me
	return render_template('/admin/edit_profile.html',form=form)

@admin.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.username = form.username.data
		user.email = form.email.data
		user.confirmed = form.confirmed.data
		user.name = form.name.data
		user.role = Role.query.get(form.role.data)
		user.department = form.department.data
		user.about_me = form.about_me.data
		db.session.add(user)
		flash('updated success','success')
		return redirect(url_for('.user', username=user.username))
	form.username.data = user.username
	form.email.data = user.email
	form.confirmed.data = user.confirmed
	form.name.data = user.name
	form.role.data = user.role
	form.department.data = user.department
	form.about_me.data = user.about_me
	return render_template('/admin/edit_profile.html',form=form)

@admin.route('/admin/account_manage.html',methods=['GET','POST'])
@login_required
@admin_required
def account_manage():

	form = EditUserForm()
	accounts = User.query.order_by(User.id).all()
	return render_template('/admin/account_manage.html',accounts=accounts,form=form)

@admin.route('/get_user_info/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def get_user_info(id):
	user = User.query.get_or_404(id)
	return jsonify({
		'id':user.id,
		'username':user.username,
		'email':user.email,
		'confirmed':user.confirmed,
		'role':user.role.id,
		'name':user.name,
		'department':user.department,
		'about_me':user.about_me
	})

@admin.route('/admin/edit_user_info/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_user_info(id):
	user = User.query.get_or_404(id)
	form = EditUserForm()
	if form.validate_on_submit():
		user.username = form.username.data
		user.email = form.email.data
		user.confirmed = form.confirmed.data
		user.name = form.name.data
		user.role = Role.query.get(form.role.data)
		user.department = form.department.data
		user.about_me = form.about_me.data
		try:
			db.session.commit()
		except:
			db.session.rollback()
			flash(u'更新失败！', 'danger')
		else:
			flash(u'更新成功！', 'success')
		return redirect(url_for('.account_manage'))
	return redirect(url_for('.account_manage'))


@admin.route('/delete_user/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def delete_user(id):
	user = User.query.get_or_404(id)
	db.session.delete(user)
	try:
		db.session.commit()
	except:
		db.session.rollback()
		flash(u'删除失败！', 'danger')
	else:
		flash(u'删除成功！', 'success')
	return	redirect(url_for('.account_manage'))


