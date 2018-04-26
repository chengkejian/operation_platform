#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: forms.py
@time: 2016/8/30 15:48
"""
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,IntegerField,RadioField,SelectField
from wtforms import validators
from flask_pagedown.fields import PageDownField
from app import db
from ..models import AndroidChannel

class NameFrom(FlaskForm):
	name = StringField('NAME',[validators.DataRequired(), validators.length(max=10)])
	passwd = PasswordField('PASSWORD',[validators.DataRequired()])
	submit = SubmitField('Submit')

class SearchForm(FlaskForm):
	channleId = IntegerField(u'查找',[validators.DataRequired()])
	submit = SubmitField('Submit')

class PostForm(FlaskForm):
	body = PageDownField(u'添加说明',[validators.DataRequired()])
	submit = SubmitField('Submit')

class Post_EditForm(PostForm):
	body = PageDownField(u'编辑说明',[validators.DataRequired()])
	submit = SubmitField('Submit')

class Channels_DeleteForm(FlaskForm):
	del_channelIds = StringField([validators.DataRequired()])

class Channels_AddForm(FlaskForm):
	channel_name = StringField(u'渠道名称',[validators.DataRequired()])
	channel = IntegerField(u'渠道号',[validators.DataRequired(),validators.length(max=10)])
	app_name = StringField(u'安装包名',[validators.DataRequired(),validators.length(max=10)])
	package_link = RadioField(u'包or链接：',coerce=int,choices=[(1,'Package'),(2,'Link')])
	need_replace_ico = RadioField(u'是否替换图标：',coerce=int,choices=[(1,'Yes'),(0,'No')])
	# images= FileField(u'图标')
	version = StringField(u'版本',[validators.DataRequired()])

class Channels_EditForm(FlaskForm):
	edit_channel_name = StringField(u'渠道名称',[validators.DataRequired()])
	edit_channel = IntegerField(u'渠道号',[validators.DataRequired(),validators.length(max=10)])
	edit_app_name = StringField(u'安装包名',[validators.DataRequired(),validators.length(max=10)])
	edit_package_link = RadioField(u'包or链接：',coerce=int,choices=[(1,'Package'),(2,'Link')])
	edit_need_replace_ico = RadioField(u'是否替换图标：',coerce=int,choices=[(1,'Yes'),(0,'No')])
	edit_version = StringField(u'版本',[validators.DataRequired()])

class Channels_EditVersionForm(FlaskForm):
	edit_channelIds = StringField([validators.DataRequired()])
	edit_version = StringField(u'版本号:',[validators.DataRequired()])

class Channels_PackageForm(FlaskForm):
	pkg_channelIds = StringField([validators.DataRequired()])

class Allchannels_PackageForm(FlaskForm):
	version = SelectField(u'打包版本:', coerce=str)
	to_version = StringField(u'更新到:',[validators.DataRequired()])
	def __init__(self,*args, **kwargs):
		super(Allchannels_PackageForm, self).__init__(*args, **kwargs)
		self.version.choices = [('all',u'全部版本')]
	def insert_version(self,platform):
		versions = list(db.session.query(AndroidChannel.version).filter_by(platform=platform)\
					   .order_by(AndroidChannel.version.desc()).distinct().all())
		for i in versions:
			self.version.choices.append((str(i[0]),str(i[0])))


class Package_UploadForm(FlaskForm):
	pub_channelIds = StringField([validators.DataRequired()])

class allPackage_UploadForm(FlaskForm):
	version = SelectField(u'发布版本:', coerce=str)
	def __init__(self,*args, **kwargs):
		super(allPackage_UploadForm, self).__init__(*args, **kwargs)
		self.version.choices = []
	def insert_version(self,platform):
		versions = list(db.session.query(AndroidChannel.version).filter_by(platform=platform)\
					   .filter_by(package_link='link').order_by(AndroidChannel.version.desc()).distinct().all())
		for i in versions:
			self.version.choices.append((str(i[0]),str(i[0])))


class Channel_FilterForm(FlaskForm):
	package_link = SelectField(u'包or链接:', coerce=str)
	replace_ico = SelectField(u'替换图标:', coerce=int)
	package_status = SelectField(u'打包状态:', coerce=int)
	package_upload_status = SelectField(u'发布状态:', coerce=int)
	version = SelectField(u'版本号:', coerce=str)
	def __init__(self,*args, **kwargs):
		super(Channel_FilterForm, self).__init__(*args, **kwargs)
		self.package_link.choices = [('all',u'全部类型'),('package',u'包'),('link',u'链接')]
		self.replace_ico.choices = [(3,u'全部'),(1,u'是'),(0,u'否')]
		self.package_status.choices = [(4,u'全部'),(0,u'未打包'),(1,u'正在打包'),(2,u'打包成功'),(3,u'打包失败')]
		self.package_upload_status.choices = [(4,u'全部'),(0,u'未发布'),(1,u'正在发布'),(2,u'发布成功'),(3,u'发布失败')]
		self.version.choices = [('all',u'全部版本')]
	def insert_version(self,platform):
		versions = list(db.session.query(AndroidChannel.version).filter_by(platform=platform)\
					   .order_by(AndroidChannel.version.desc()).distinct().all())
		for i in versions:
			self.version.choices.append((str(i[0]),str(i[0])))



