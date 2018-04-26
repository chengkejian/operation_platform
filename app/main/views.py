#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: views.py
@time: 2016/8/23 14:41
"""
import json,os,shutil,logging
from flask import render_template,session,url_for,flash,redirect,current_app,request,abort,jsonify,send_from_directory
from datetime import datetime
from . import main
from .forms import PostForm,Post_EditForm,SearchForm,Channels_DeleteForm,Channels_AddForm,\
	Channels_EditForm,Channels_PackageForm,Channels_EditVersionForm,Package_UploadForm,Channel_FilterForm,\
	Allchannels_PackageForm,allPackage_UploadForm
from .. import db
from ..models import Post,Permission,AndroidChannel,AndroidPlatform
from ..email import send_email
from flask_login  import login_required,current_user
from ..decorators import admin_required,permission_required
from werkzeug.utils import secure_filename

logger = logging.getLogger("mobim")

@main.route('/',methods=['GET','POST'])
@login_required
def index():
	return render_template('index.html', name=session.get('name'))


@main.route('/android/androidstep.html',methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ANDROIDSTEP)
def androidstep():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data,author=current_user._get_current_object())
		db.session.add(post)
		flash(u'添加成功')
		return redirect(url_for('.androidstep'))
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
			page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
			error_out=False)
	posts = pagination.items
	return render_template('/android/androidstep.html',form=form,posts=posts,pagination=pagination,permission=Permission.ANDROID)


@main.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ANDROIDSTEP)
def edit_post(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and  not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = Post_EditForm()
	if form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		flash(u'更新成功')
		return redirect(url_for('.androidstep'))
	form.body.data = post.body
	return render_template('/android/edit_post.html',form=form)

@main.route('/delete_post/<int:id>',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROIDSTEP)
def delete_post(id):
	post = Post.query.get_or_404(id)
	db.session.delete(post)
	try:
		db.session.commit()
	except Exception,e:
		logger.error(e)
		db.session.rollback()
		flash(u'删除失败！', 'danger')
	else:
		flash(u'删除成功！', 'success')
	return	redirect(url_for('.androidstep'))

# @main.route('/android/androidpack/<string:platform>',methods=['GET','POST'])
# @login_required
# @permission_required(Permission.ANDROID)
# def androidpack(platform):
# 	form = SearchForm()
# 	del_form = Channels_DeleteForm()
# 	pkg_form = Channels_PackageForm()
# 	edit_cnlver_form = Channels_EditVersionForm()
# 	pkgs_upload_form = Package_UploadForm()
# 	add_cnl_form = Channels_AddForm()
# 	edit_cnl_form =Channels_EditForm()
# 	filter_cnl_form = Channel_FilterForm()
# 	platnames = AndroidPlatform.query.order_by(AndroidPlatform.id).all()
# 	platform=platform
# 	filter_cnl_form.insert_version(str(platform))
# 	page = request.args.get('page', 1, type=int)
# 	pagination = AndroidChannel.query.filter_by(platform=platform).order_by(AndroidChannel.version.desc()).paginate(
# 			page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
# 			error_out=False)
# 	androids = pagination.items
# 	return render_template('/android/androidpack.html',pagination=pagination,androids=androids,
# 						   platform=platform,platnames=platnames,form=form,del_form=del_form,
# 						   pkg_form=pkg_form,edit_cnlver_form=edit_cnlver_form,pkgs_upload_form=pkgs_upload_form,
# 						   add_cnl_form=add_cnl_form,edit_cnl_form=edit_cnl_form,filter_cnl_form=filter_cnl_form)

@main.route('/android/search/<string:platform>',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def androidsearch(platform):
	form = SearchForm()
	del_form = Channels_DeleteForm()
	pkg_form = Channels_PackageForm()
	all_pkg_form = Allchannels_PackageForm()
	all_pkg_form.insert_version(str(platform))
	all_pub_form = allPackage_UploadForm()
	all_pub_form.insert_version(str(platform))
	pkgs_upload_form = Package_UploadForm()
	edit_cnlver_form = Channels_EditVersionForm()
	add_cnl_form = Channels_AddForm()
	edit_cnl_form =Channels_EditForm()
	filter_cnl_form = Channel_FilterForm()
	filter_cnl_form.insert_version(str(platform))
	platnames = AndroidPlatform.query.order_by(AndroidPlatform.id).all()
	platform=platform
	page = request.args.get('page', 1, type=int)
	if form.validate_on_submit():
		pagination = AndroidChannel.query.filter_by(platform=platform).filter_by(channel=form.channleId.data).paginate(
				page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
				error_out=False)
		androids = pagination.items
		return render_template('/android/androidpack.html',pagination=pagination,androids=androids,
							   platform=platform,platnames=platnames,form=form,del_form=del_form,
							   pkg_form=pkg_form,edit_cnlver_form=edit_cnlver_form,pkgs_upload_form=pkgs_upload_form,
							   add_cnl_form=add_cnl_form,edit_cnl_form=edit_cnl_form,filter_cnl_form=filter_cnl_form,
							   all_pkg_form=all_pkg_form,all_pub_form=all_pub_form)
	return 	redirect(url_for('.androidpack',platform='official'))

@main.route('/android/androidpack/<string:platform>',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def androidpack(platform):
	platform=platform
	page = request.args.get('page', 1, type=int)
	version = request.args.get('version','all', type=str)
	package_link = request.args.get('package_link','all', type=str)
	replace_ico = request.args.get('replace_ico',3, type=int)
	package_status = request.args.get('package_status',4, type=int)
	package_upload_status = request.args.get('package_upload_status',4, type=int)
	form = SearchForm()
	del_form = Channels_DeleteForm()
	pkg_form = Channels_PackageForm()
	all_pkg_form = Allchannels_PackageForm()
	all_pkg_form.insert_version(str(platform))
	all_pub_form = allPackage_UploadForm()
	all_pub_form.insert_version(str(platform))
	edit_cnlver_form = Channels_EditVersionForm()
	pkgs_upload_form = Package_UploadForm()
	add_cnl_form = Channels_AddForm()
	edit_cnl_form =Channels_EditForm()
	filter_cnl_form = Channel_FilterForm()
	filter_cnl_form.insert_version(str(platform))
	platnames = AndroidPlatform.query.order_by(AndroidPlatform.id).all()
	result = AndroidChannel.query.filter_by(platform=platform)
	if filter_cnl_form.validate_on_submit():
		if filter_cnl_form.package_link.data != 'all':
			package_link = filter_cnl_form.package_link.data
			result = result.filter_by(package_link=filter_cnl_form.package_link.data)
		if filter_cnl_form.replace_ico.data != 3:
			replace_ico = filter_cnl_form.replace_ico.data
			result = result.filter_by(need_replace_ico=bool(filter_cnl_form.replace_ico.data))
		if filter_cnl_form.version.data !='all':
			version = filter_cnl_form.version.data
			result = result.filter_by(version=filter_cnl_form.version.data)
		if filter_cnl_form.package_status.data != 4:
			package_status = filter_cnl_form.package_status.data
			result = result.filter_by(package_status=filter_cnl_form.package_status.data)
		if filter_cnl_form.package_upload_status.data != 4:
			package_upload_status = filter_cnl_form.package_upload_status.data
			result = result.filter_by(package_upload_status=filter_cnl_form.package_upload_status.data)

	else:
		if package_link != 'all':
			result = result.filter_by(package_link=package_link)
		if replace_ico != 3:
			result = result.filter_by(need_replace_ico=bool(replace_ico))
		if version != 'all':
			result = result.filter_by(version=version)
		if package_status != 4:
			result = result.filter_by(package_status=package_status)
		if package_upload_status != 4:
			result = result.filter_by(package_upload_status=package_upload_status)
	pagination = result.order_by(AndroidChannel.version.desc()).\
		paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	androids = pagination.items
	return 	render_template('/android/androidpack.html',pagination=pagination,androids=androids,
							  version=version,replace_ico=replace_ico,package_link=package_link,
							  package_status=package_status,package_upload_status=package_upload_status,
							   platform=platform,platnames=platnames,form=form,del_form=del_form,
							   pkg_form=pkg_form,edit_cnlver_form=edit_cnlver_form,pkgs_upload_form=pkgs_upload_form,
							   add_cnl_form=add_cnl_form,edit_cnl_form=edit_cnl_form,filter_cnl_form=filter_cnl_form,
							  all_pkg_form=all_pkg_form,all_pub_form=all_pub_form)

@main.route('/android/package_status',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def package_status():
	platform = request.args.get('platform')
	package_now = AndroidChannel.query.filter_by(platform=platform).filter_by(package_status=1).count()
	package_error = AndroidChannel.query.filter_by(platform=platform).filter_by(package_status=3).count()
	upload_now = AndroidChannel.query.filter_by(platform=platform).filter_by(package_upload_status=1).count()
	upload_error = AndroidChannel.query.filter_by(platform=platform).filter_by(package_upload_status=3).count()

	return jsonify({'package_now': package_now,
					'package_error': package_error,
					'upload_now': upload_now,
					'upload_error': upload_error})

@main.route('/android/delete_channel/<int:id>',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def delete_channel(id):
	channel = AndroidChannel.query.get_or_404(id)
	platform = channel.platform
	page = request.args.get('page',type=int)
	db.session.delete(channel)
	try:
		db.session.commit()
	except Exception,e:
		logger.error(e)
		db.session.rollback()
		flash(u'删除失败！', 'danger')
	else:
		if channel.need_replace_ico:
			img_path = current_app.config['UPLOAD_FOLDER']+'/native_R'+channel.version+'/channelIco'+'/%s' %(str(channel.channel)+'-'+platform)
			if  os.path.exists(img_path):
				shutil.rmtree(img_path)
		flash(u'删除成功！', 'success')
	return	redirect(url_for('.androidpack',platform=platform,page=page))

@main.route('/android/delete_channels',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def delete_channels():
	page = request.args.get('page',type=int)
	platform = request.args.get('platform')
	form = Channels_DeleteForm()
	if form.validate_on_submit():
		channelsIds =json.loads(form.del_channelIds.data)
		deleted=0
		for id in channelsIds:
			channel = AndroidChannel.query.get_or_404(id)
			db.session.delete(channel)
			try:
				db.session.commit()
			except Exception,e:
				logger.error(e)
				db.session.rollback()
				flash(u'删除失败！', 'danger')
			else:
				if channel.need_replace_ico:
					img_path = current_app.config['UPLOAD_FOLDER']+'/native_R'+channel.version+'/channelIco'+'/%s' %(str(channel.channel)+'-'+platform)
					if  os.path.exists(img_path):
						shutil.rmtree(img_path)
				deleted +=1
		flash(u'成功删除 %d 个渠道 ' %(deleted),'success')
	return redirect(url_for('.androidpack',platform=platform,page=page))

@main.route('/android/add_channel',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def add_channel():
	page = request.args.get('page',type=int)
	platform = request.args.get('platform')
	if request.method == 'POST':
		channel_name = request.form['channel_name']
		channel = request.form['channel']
		app_name = request.form['app_name']
		package_link = 'package' if request.form['package_link'] == '1' else 'link'
		version = request.form['version']
		need_replace_ico = request.form['need_replace_ico']

		channel_get = AndroidChannel.query.filter_by(channel=channel).filter_by(platform=platform).first()
		if channel_get is None:
			if need_replace_ico == '1':
				img_path = current_app.config['UPLOAD_FOLDER']+'/native_R'+version+'/channelIco'+'/%s' %(channel+'-'+platform)
				img_tmp=current_app.config['UPLOAD_FOLDER']+'/tmp'
				if  os.path.exists(img_path):
					shutil.rmtree(img_path)
				if os.path.exists(img_tmp):
					os.rename(img_tmp,img_path)
				else:
					flash(u'渠道添加失败(图标未上传)','danger')
					return redirect(url_for('.androidpack',platform=platform,page=page))
			android_channel = AndroidChannel(channel_name=channel_name,channel=channel,app_name=app_name,
										 package_link=package_link,need_replace_ico=int(need_replace_ico),
										 version=version,platform=platform,package_status=0,package_upload_status=0)
			db.session.add(android_channel)
			try:
				db.session.commit()
			except Exception,e:
				logger.error(e)
				db.session.rollback()
				flash(u'添加渠道失败！', 'danger')
			else:
				flash(u'添加渠道成功','success')
				return redirect(url_for('.androidpack',platform=platform,page=page))
		else:
			flash(u'渠道号已经存在！','info')
	flash(u'添加渠道失败！', 'danger')
	return	redirect(url_for('.androidpack',platform=platform,page=page))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/android/img_upload',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def img_upload():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			img_tmp=current_app.config['UPLOAD_FOLDER']+'/tmp'
			if not os.path.exists(img_tmp):
				os.makedirs(img_tmp)
			filename = secure_filename(file.filename)
			file.save(os.path.join(img_tmp,filename))
			return jsonify({'message':u'成功'})
	return jsonify({'error':u'失败'})

@main.route('/android/get_channel_info/<int:id>',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def get_channel_info(id):
	channel = AndroidChannel.query.get_or_404(id)
	return jsonify({
		'id':channel.id,
		'channelname':channel.channel_name,
		'channel':channel.channel,
		'app_name':channel.app_name,
		'package_link':channel.package_link,
		'need_replace_ico':channel.need_replace_ico,
		'version':channel.version,
		'platform':channel.platform,
		'page':request.args.get('page',type=int)
	})

@main.route('/android/edit_channel_info/<int:id>',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def edit_channel_info(id):
	page = request.args.get('page',type=int)
	android_channel = AndroidChannel.query.get_or_404(id)
	if request.method == 'POST':
		channel_name = request.form['edit_channel_name']
		channel = request.form['edit_channel']
		version = request.form['edit_version']
		app_name = request.form['edit_app_name']
		package_link = 'package' if request.form['edit_package_link'] == '1' else 'link'
		need_replace_ico = int(request.form['edit_need_replace_ico'])
		img_path = current_app.config['UPLOAD_FOLDER']+'/native_R'+version+'/channelIco'+'/%s' %(channel+'-'+android_channel.platform)
		img_tmp=current_app.config['UPLOAD_FOLDER']+'/tmp'
		if need_replace_ico:
			if not os.path.exists(img_path):
				flash(u'渠道修改失败(此版本不存在)','danger')
				return  redirect(url_for('.androidpack',platform=android_channel.platform,page=page))
			elif not os.path.exists(img_tmp):
				flash(u'渠道修改失败(图标未上传)','danger')
				return  redirect(url_for('.androidpack',platform=android_channel.platform,page=page))
		if android_channel.channel == int(channel):
			android_channel.channel_name=channel_name
			android_channel.version=version
			android_channel.app_name=app_name
			android_channel.package_link=package_link
			android_channel.need_replace_ico=need_replace_ico
			android_channel.package_status=0
			android_channel.package_upload_status=0
			db.session.add(android_channel)
			try:
				db.session.commit()
			except Exception,e:
				logger.error(e)
				db.session.rollback()
				flash(u'渠道修改失败！', 'danger')
			else:
				flash(u'渠道修改成功','success')
				if need_replace_ico:
					if os.path.exists(img_tmp):
						try:
							shutil.rmtree(img_path)
						except:pass
						os.rename(img_tmp,img_path)
				else:
					try:
						shutil.rmtree(img_path)
					except:pass
				return redirect(url_for('.androidpack',platform=android_channel.platform,page=page))
		else:
			channel_get = AndroidChannel.query.filter_by(channel=channel).filter_by(platform=android_channel.platform).first()
			if channel_get is None:
				android_channel.channel=channel
				android_channel.channel_name=channel_name
				android_channel.version=version
				android_channel.app_name=app_name
				android_channel.package_link=package_link
				android_channel.need_replace_ico=need_replace_ico
				android_channel.package_status=0
				android_channel.package_upload_status=0
				db.session.add(android_channel)
				try:
					db.session.commit()
				except:
					db.session.rollback()
					flash(u'渠道修改失败！', 'danger')
				else:
					flash(u'渠道修改成功','success')
					if need_replace_ico:
						img_path2=current_app.config['UPLOAD_FOLDER']+'/native_R'+version+'/channelIco'+'/%s' %(channel+'-'+android_channel.platform)
						if os.path.exists(img_tmp):
							shutil.rmtree(img_path)

							os.rename(img_tmp,img_path2)
					else:
						try:
							shutil.rmtree(img_path)
						except:pass
				return redirect(url_for('.androidpack',platform=android_channel.platform,page=page))
			else:
				flash(u'渠道号已经存在！','info')
	flash(u'渠道修改失败！', 'danger')
	return	redirect(url_for('.androidpack',platform=android_channel.platform,page=page))


@main.route('/android/edit_channels_version',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def edit_channels_version():
	page = request.args.get('page',type=int)
	platform = request.args.get('platform')
	if request.method == 'POST':
		channelsIds =json.loads(request.form['edit_channelIds'])
		version = request.form['edit_version']
		for id in channelsIds:
			android_channel = AndroidChannel.query.get_or_404(id)
			android_channel.version=version
			android_channel.package_status=0
			android_channel.package_upload_status=0
			db.session.add(android_channel)
		try:
				db.session.commit()
		except Exception,e:
				logger.error(e)
				db.session.rollback()
				flash(u'渠道版本修改失败!!!', 'danger')
		else:
				flash(u'渠道版本修改成功！','success')
	return	redirect(url_for('.androidpack',platform=platform,page=page))

@main.route('/android/channel_package/<int:id>',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def channel_package(id):
	import android_common
	mysql_connect = android_common.Mysql_for_AndroidChannel()
	page = request.args.get('page',type=int)
	android_channel = AndroidChannel.query.get_or_404(id)
	android_platform = AndroidPlatform.query.filter_by(platform=android_channel.platform).first()
	project_root = current_app.config['PROJECT_ROOT']
	package_root = current_app.config['PACKAGE_ROOT']
	if not os.path.exists(project_root+android_channel.version):
		flash(u'此版本暂未发布，请联系管理员','info')
		return redirect(url_for('.androidpack',platform=android_channel.platform,page=page))
	try:
		mysql_connect.setPackageStatus(android_channel.id,1)
		mysql_connect.setPackageUploadStatus(android_channel.id,0)
	finally:mysql_connect.session_close()
	android_common.androidPackage(project_root,package_root,1)
	return redirect(url_for('.androidpack',platform=android_channel.platform,page=page))

@main.route('/android/select_channels_package',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def select_channels_package():
	import android_common
	mysql_connect = android_common.Mysql_for_AndroidChannel()
	page = request.args.get('page',type=int)
	platform = request.args.get('platform')
	select_form = Channels_PackageForm()
	if select_form.validate_on_submit():
		channelsIds =json.loads(select_form.pkg_channelIds.data)
		noChannelVersion={}
		count = 1
		try:
			for id in channelsIds:
				android_channel = AndroidChannel.query.get_or_404(id)
				project_root = current_app.config['PROJECT_ROOT']
				package_root = current_app.config['PACKAGE_ROOT']
				if not os.path.exists(project_root+android_channel.version):
					noChannelVersion[android_channel.channel] = android_channel.version
					continue
				mysql_connect.setPackageStatus(android_channel.id,1)
				mysql_connect.setPackageUploadStatus(android_channel.id,0)
				android_common.androidPackage(project_root,package_root,count)
				count +=1
		finally:mysql_connect.session_close()
		if noChannelVersion:
			for k,v in noChannelVersion.iteritems():
				flash(u'渠道号为 %s 的 %s 版本暂未发布，请联系管理员' %(k,v) )
		return redirect(url_for('.androidpack',platform=platform,page=page))
	return redirect(url_for('.androidpack',platform=platform,page=page))

@main.route('/android/all_channels_package',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def all_channels_package():
	import android_common
	mysql_connect = android_common.Mysql_for_AndroidChannel()
	page = request.args.get('page',type=int)
	platform = request.args.get('platform')
	project_root = current_app.config['PROJECT_ROOT']
	package_root = current_app.config['PACKAGE_ROOT']
	package_now = 1
	count = 1
	if request.method == 'POST':
		version = request.form['version']
		to_version = request.form['to_version']
		if not os.path.exists(project_root+to_version):
			flash(u'%s 版本暂未发布，请联系管理员' %(to_version),'danger')
			return redirect(url_for('.androidpack',platform=platform,page=page))
		if version=='all':
			channels = AndroidChannel.query.filter_by(platform=platform).all()
		else:
			channels = AndroidChannel.query.filter_by(platform=platform).filter_by(version=version).all()
		try:
			for channel in channels:
				channel.version=to_version
				mysql_connect.setPackageStatus(channel.id,1)
				mysql_connect.setPackageUploadStatus(channel.id,0)
				if package_now < 4:
					android_common.androidPackage(project_root,package_root,count)
				package_now +=1
				count+=1
		finally:mysql_connect.session_close()
	return redirect(url_for('.androidpack',platform=platform,page=page))



@main.route('/android/package_download/<int:id>',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def package_download(id):
	page = request.args.get('page',type=int)
	android_channel = AndroidChannel.query.get_or_404(id)
	pkgpath = os.path.join(current_app.config['PACKAGE_ROOT'],android_channel.version)
	pkgname = 'imifun' if android_channel.package_name==None else android_channel.package_name
	if not os.path.exists(os.path.join(pkgpath,pkgname)):
		flash(u'没有 %s 渠道的 %s 版本，请先打包！' %(android_channel.channel,android_channel.version),'warning')
		return redirect(url_for('.androidpack',platform=android_channel.platform,page=page))
	return send_from_directory(pkgpath,pkgname,as_attachment=True)

@main.route('/android/package_upload/<int:id>',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def package_upload(id):
	import android_common
	mysql_connect = android_common.Mysql_for_AndroidChannel()
	page = request.args.get('page',type=int)
	android_channel = AndroidChannel.query.get_or_404(id)
	pkgpath = os.path.join(current_app.config['PACKAGE_ROOT'],android_channel.version)
	pkgname = 'imifun' if android_channel.package_name==None else android_channel.package_name
	try:
		if not os.path.exists(os.path.join(pkgpath,pkgname)):
			flash(u'没有 %s 渠道的 %s 版本，请先打包！' %(android_channel.channel,android_channel.version),'warning')
			return redirect(url_for('.androidpack',platform=android_channel.platform,page=page))
		if android_channel.platform=='yunfan':
			mysql_connect.setPackageUploadStatus(android_channel.id,1)
			idForup = 1 if mysql_connect.getChannel_uploadSum_Yunfan(android_channel.platform)==1 else 2
			if idForup ==1:
				android_common.uploadPackage_Yunfan(current_app.config['YUNFAN_PACKAGE_FTP_IP'],current_app.config['YUNFAN_PACKAGE_FTP_PORT'],
											   current_app.config['YUNFAN_PACKAGE_FTP_USER'],current_app.config['YUNFAN_PACKAGE_FTP_PASSWD'],
											   android_channel.platform,pkgpath,current_app.config['YUNFAN_PACKAGE_SFTP_PATH'])
		else:
			if android_channel.platform=='official' and (android_channel.channel==8000 or android_channel.channel==7999) \
				or android_channel.platform=='qq' or android_channel.platform=='official_entertainment' and android_channel.channel==7999:
				remotepath = current_app.config['IMIFUN_PACKAGE_SFTP_PATH']+'/ivp/down/'
			else:remotepath = current_app.config['IMIFUN_PACKAGE_SFTP_PATH']+'/tg/'

			mysql_connect.setPackageUploadStatus(android_channel.id,1)
			idForup = 1 if mysql_connect.getChannel_uploadSum(android_channel.platform)==1 else 2
			if idForup == 1 or android_channel.channel==8000 or android_channel.channel==7999:
				android_common.uploadPackage_Imifun(idForup,current_app.config['IMIFUN_PACKAGE_SFTP_IP'],current_app.config['IMIFUN_PACKAGE_SFTP_PORT'],
									current_app.config['IMIFUN_PACKAGE_SFTP_USER'],current_app.config['IMIFUN_PACKAGE_SFTP_PASSWD'],
								 android_channel.id,android_channel.package_name,android_channel.platform,android_channel.channel,
												pkgpath,remotepath)
	finally:mysql_connect.session_close()
	return redirect(url_for('.androidpack',platform=android_channel.platform,page=page))

@main.route('/android/select_packages_upload',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def select_packages_upload():
	import android_common
	mysql_connect = android_common.Mysql_for_AndroidChannel()
	page = request.args.get('page',type=int)
	platform = request.args.get('platform')
	if request.method == 'POST':
		channelsIds =json.loads(request.form['pub_channelIds'])
		noChannelPackage={}
		ChannelIsPackage=[]
		try:
			for id in channelsIds:
				android_channel = AndroidChannel.query.get_or_404(id)
				pkgpath = os.path.join(current_app.config['PACKAGE_ROOT'],android_channel.version)
				pkgname = 'imifun' if android_channel.package_name==None else android_channel.package_name
				if not os.path.exists(os.path.join(pkgpath,pkgname)):
					noChannelPackage[android_channel.channel] = android_channel.version
					continue
				if android_channel.package_link=='package':
					ChannelIsPackage.append(int(android_channel.channel))
					continue
				if android_channel.platform=='yunfan':
					mysql_connect.setPackageUploadStatus(android_channel.id,1)
					idForup = 1 if mysql_connect.getChannel_uploadSum_Yunfan(android_channel.platform)==1 else 2
					if idForup ==1:
						android_common.uploadPackage_Yunfan(current_app.config['YUNFAN_PACKAGE_FTP_IP'],current_app.config['YUNFAN_PACKAGE_FTP_PORT'],
											   current_app.config['YUNFAN_PACKAGE_FTP_USER'],current_app.config['YUNFAN_PACKAGE_FTP_PASSWD'],
											   android_channel.platform,pkgpath,current_app.config['YUNFAN_PACKAGE_SFTP_PATH'])
				else:
					if android_channel.platform=='official' and (android_channel.channel==8000 or android_channel.channel==7999) \
						or android_channel.platform=='qq' or android_channel.platform=='official_entertainment' and android_channel.channel==7999:
						remotepath = current_app.config['IMIFUN_PACKAGE_SFTP_PATH']+'/ivp/down/'
					else:remotepath = current_app.config['IMIFUN_PACKAGE_SFTP_PATH']+'/tg/'

					mysql_connect.setPackageUploadStatus(android_channel.id,1)
					idForup = 1 if mysql_connect.getChannel_uploadSum(android_channel.platform)==1 else 2
					if idForup == 1 or android_channel.channel==8000 or android_channel.channel==7999:
						android_common.uploadPackage_Imifun(idForup,current_app.config['IMIFUN_PACKAGE_SFTP_IP'],current_app.config['IMIFUN_PACKAGE_SFTP_PORT'],
									current_app.config['IMIFUN_PACKAGE_SFTP_USER'],current_app.config['IMIFUN_PACKAGE_SFTP_PASSWD'],
								 android_channel.id,android_channel.package_name,platform,
								android_channel.channel,pkgpath,remotepath)
		finally:mysql_connect.session_close()
		if noChannelPackage:
			for k,v in noChannelPackage.iteritems():
				flash(u'渠道号为 %s 的 %s 版本暂未打包，请打包后发布！' %(k,v),'warning')
		if ChannelIsPackage:
				flash(u'渠道号为 %s 为Package类型，若要发布，请修改 “包or链接” 为Link！' %ChannelIsPackage,'warning')
	return redirect(url_for('.androidpack',platform=platform,page=page))

@main.route('/android/all_packages_upload',methods=['GET','POST'])
@login_required
@permission_required(Permission.ANDROID)
def all_packages_upload():
	import android_common
	mysql_connect = android_common.Mysql_for_AndroidChannel()
	page = request.args.get('page',type=int)
	platform = request.args.get('platform')
	if request.method == 'POST':
		version =request.form['version']
		channels = AndroidChannel.query.filter_by(platform=platform).filter_by(version=version).\
					filter_by(package_link='link').all()
		noChannelPackage=[]
		pkgpath = os.path.join(current_app.config['PACKAGE_ROOT'],version)
		try:
			for channel in channels:
				pkgname = 'imifun' if channel.package_name==None else channel.package_name
				if not os.path.exists(os.path.join(pkgpath,pkgname)):
					noChannelPackage.append(int(channel.channel))
					continue
				if channel.platform=='yunfan':
					mysql_connect.setPackageUploadStatus(channel.id,1)
					idForup = 1 if mysql_connect.getChannel_uploadSum_Yunfan(channel.platform)==1 else 2
					if idForup ==1:
						android_common.uploadPackage_Yunfan(current_app.config['YUNFAN_PACKAGE_FTP_IP'],current_app.config['YUNFAN_PACKAGE_FTP_PORT'],
											   current_app.config['YUNFAN_PACKAGE_FTP_USER'],current_app.config['YUNFAN_PACKAGE_FTP_PASSWD'],
											   channel.platform,pkgpath,current_app.config['YUNFAN_PACKAGE_SFTP_PATH'])
				else:
					if platform=='official' and (channel.channel==8000 or channel.channel==7999) \
						or platform=='qq' or platform=='official_entertainment' and channel.channel==7999:
						remotepath = current_app.config['IMIFUN_PACKAGE_SFTP_PATH']+'/ivp/down/'
					else:remotepath = current_app.config['IMIFUN_PACKAGE_SFTP_PATH']+'/tg/'

					mysql_connect.setPackageUploadStatus(channel.id,1)
					idForup = 1 if mysql_connect.getChannel_uploadSum(channel.platform)==1 else 2
					if idForup == 1 or channel.channel==8000 or channel.channel==7999:
						android_common.uploadPackage_Imifun(idForup,current_app.config['IMIFUN_PACKAGE_SFTP_IP'],current_app.config['IMIFUN_PACKAGE_SFTP_PORT'],
									current_app.config['IMIFUN_PACKAGE_SFTP_USER'],current_app.config['IMIFUN_PACKAGE_SFTP_PASSWD'],
								 channel.id,channel.package_name,platform,channel.channel,pkgpath,remotepath)
		finally:mysql_connect.session_close()
		if noChannelPackage:
				flash(u'渠道号为 %s 的 %s 版本暂未打包，请打包后发布！' %(noChannelPackage,version),'warning')
	return redirect(url_for('.androidpack',platform=platform,page=page))


@main.route('/ios/iosstep.html')
@login_required
@permission_required(Permission.IOSSTEP)
def iosstep():
	return render_template('/ios/iosstep.html',current_time=datetime.utcnow())


@main.route('/ios/iospack.html')
@login_required
@permission_required(Permission.IOS)
def iospack():
	return render_template('/ios/iospack.html')

@main.route('/ios/iospublish.html')
@login_required
@permission_required(Permission.IOS)
def iospublish():
	return render_template('/ios/iospublish.html')