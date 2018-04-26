#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: android_common.py
@time: 2016/12/20 13:43
"""

import os,time,shutil,zipfile,ftplib
import logging
import paramiko,pysftp
import threading
from ..models import AndroidChannel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("mobim")


def androidPackage(project_root,package_root,count):
	thr = MyThread(project_root,package_root,count)
	thr.start()
	return thr

class MyThread(threading.Thread):
	def __init__(self,project_root,package_root,count):
		threading.Thread.__init__(self)
		self.project_root = project_root
		self.package_root = package_root
		self.count = count
	def run(self):
		if self.count !=1:time.sleep(3)
		mysql_connect=Mysql_for_AndroidChannel()
		gradle_pid=get_gradle()
		try:
			if mysql_connect.getChannel_packageSum() > 1 and int(gradle_pid) != 256:
				pass
			else:
				while mysql_connect.getChannel_packageSum():

					channel = mysql_connect.getChannel_package()
					status=android_async_package(mysql_connect,self.project_root+channel.version,os.path.join(self.package_root,channel.version),
											 channel.platform.capitalize(),channel.id,channel.channel,
											 channel.platform,channel.version,channel.app_name,
											 channel.package_link,channel.need_replace_ico)
					if status:
						pass
		finally:mysql_connect.session_close()

def get_gradle():
	pid= os.system('ps aux | grep gradle | grep -v grep ')
	return pid

def android_async_package(mysql_connect,project_root,package_root,assemble_name,channel_id,channel,
				   platform,version,appName,package_link,need_replace_ico):
	data = time.strftime('%Y%m%d')
	need_replace_ico=u'yes' if need_replace_ico is True else u'no'
	channel_info={'channel':channel,'platform':platform,'version':version,'appName':appName,'package_link':package_link,
				  'need_replace_ico':need_replace_ico,'assemble_name':assemble_name,'data':data}
	command = u'gradle --daemon -Dorg.gradle.project.channel=%(channel)s ' \
	  u'-Dorg.gradle.project.platform=%(platform)s ' \
	  u'-Dorg.gradle.project.versionName=%(version)s ' \
	  u'-Dorg.gradle.project.appName=%(appName)s ' \
	  u'-Dorg.gradle.project.packageLink=%(package_link)s ' \
	  u'-Dorg.gradle.project.replace=%(need_replace_ico)s ' \
	  u'-Ddate=%(data)s clean assemble%(assemble_name)sRelease' % channel_info

	os.chdir(project_root+'/ivp50_pro')
	x = os.system(command.encode('gbk'))

	if x == 0:
		mysql_connect.setPackageStatus(channel_id,2)
		if not os.path.exists(package_root):
			os.makedirs(package_root)
		package_src = os.path.join(project_root,'apk',data) if package_link == 'package' else os.path.join(project_root,'apk',data,'link')
		try:
			src_file = [os.path.join(package_src, file) for file in os.listdir(package_src)]
			for source in src_file:
				if os.path.exists(os.path.join(package_root,os.path.basename(source))):
					os.remove(os.path.join(package_root,os.path.basename(source)))
				shutil.move(source,package_root)
			shutil.rmtree(package_src)
		except Exception,e:
			logger.error(e)
	else:mysql_connect.setPackageStatus(channel_id,3)

	mysql_connect.setPackageTime(channel_id)
	mysql_connect.setPackageName(channel_id)

	status = mysql_connect.getChannel(version)

	if not status:
		makeMapping_zip(project_root,package_root)
	return True


class Mysql_for_AndroidChannel():
	def __init__(self):
		self.engine = create_engine("mysql+mysqldb://root:centos@10.10.10.103/yunwei?charset=utf8")
		self.DBSession = sessionmaker(bind=self.engine)
		self.session = self.DBSession()
	def setPackageStatus(self,id,status):
		android_channel=self.session.query(AndroidChannel).filter(AndroidChannel.id==id).one()
		android_channel.package_status=status
		self.session.commit()
	def setPackageUploadStatus(self,id,status):
		android_channel=self.session.query(AndroidChannel).filter(AndroidChannel.id==id).one()
		android_channel.package_upload_status=status
		self.session.commit()
	def setPackageTime(self,id):
		android_channel=self.session.query(AndroidChannel).filter(AndroidChannel.id==id).one()
		android_channel.package_time=time.strftime('%Y%m%d')
		self.session.commit()
	def setPackageName(self,id):
		android_channel=self.session.query(AndroidChannel).filter(AndroidChannel.id==id).one()
		pkgname = ''
		if android_channel.platform=='official':
			if android_channel.channel==8000:pkgname='imifun_latest.apk'
			elif android_channel.channel==7999:pkgname='imifun_R%s_%s_official_upgrade.apk' %(android_channel.version,android_channel.package_time)
			else:pkgname='imifun_%s.apk' %(android_channel.channel)
		elif android_channel.platform=='yunfan':
			if android_channel.channel==8000:pkgname='mmyunfan_latest.apk'
			elif android_channel.channel==7999:pkgname='mmyunfan_R%s_%s_yunfan_upgrade.apk' %(android_channel.version,android_channel.package_time)
			else:pkgname='yunfan_%s.apk' %(android_channel.channel)
		elif android_channel.platform=='qq':
			if android_channel.channel==8000:pkgname='imifun_qq.apk'
			elif android_channel.channel==7999:pkgname='imifun_R%s_%s_qq_upgrade.apk' %(android_channel.version,android_channel.package_time)
			else:pkgname='qq_%s.apk' %(android_channel.channel)
		elif android_channel.platform=='official_7777':
			pkgname='imifun_%s.apk' %(android_channel.channel)
		elif android_channel.platform=='official_xiuroom':
			pkgname='imichat_%s.apk' %(android_channel.channel)
		elif android_channel.platform=='official_entertainment':
			pkgname='aimizb_%s.apk' %(android_channel.channel)
		elif android_channel.platform=='official_sp_zhangzhifu':
			pkgname='imi_%s.apk' %(android_channel.channel)
		elif android_channel.platform=='official_hhzb':
			pkgname='imihh_%s.apk' %(android_channel.channel)
		elif android_channel.platform=='official_adroi':
			pkgname='flavor_%s.apk' %(android_channel.channel)
		elif android_channel.platform=='yyb':
			pkgname='yyb_%s.apk' %(android_channel.channel)
		android_channel.package_name=pkgname
		self.session.commit()

	def getChannel(self,version):
		android_channel=self.session.query(AndroidChannel).filter(AndroidChannel.package_status==1).filter(AndroidChannel.version==version).all()
		return android_channel
	def getChannel_package(self):
		android_package=self.session.query(AndroidChannel).filter(AndroidChannel.package_status==1).first()
		return android_package
	def getChannel_packageSum(self):
		android_packageSum=self.session.query(AndroidChannel).filter(AndroidChannel.package_status==1).count()
		return android_packageSum
	def getChannel_upload(self,platform):
		android_package=self.session.query(AndroidChannel).filter(AndroidChannel.platform==platform).\
			filter(AndroidChannel.package_upload_status==1).filter(AndroidChannel.channel != 8000).\
			filter(AndroidChannel.channel != 7999).first()
		return android_package
	def getChannel_uploadSum(self,platform):
		android_packageSum=self.session.query(AndroidChannel).filter(AndroidChannel.platform==platform).\
			filter(AndroidChannel.package_upload_status==1).filter(AndroidChannel.channel != 8000).\
			filter(AndroidChannel.channel != 7999).count()
		return android_packageSum
	def getChannel_upload_Yunfan(self,platform):
		android_package=self.session.query(AndroidChannel).filter(AndroidChannel.platform==platform).\
			filter(AndroidChannel.package_upload_status==1).first()
		return android_package
	def getChannel_uploadSum_Yunfan(self,platform):
		android_packageSum=self.session.query(AndroidChannel).filter(AndroidChannel.platform==platform).\
			filter(AndroidChannel.package_upload_status==1).count()
		return android_packageSum
	def session_close(self):
		self.session.close()

def makeMapping_zip(project_root,package_root):
	os.chdir(package_root)
	source_dir= os.path.join(project_root,'ivp50_pro/build/outputs/mapping')
	output_filename = 'mapping_%s.zip' % (time.strftime('%Y-%m-%d_%H%M%S'))
	zipf = zipfile.ZipFile(output_filename, 'w',zipfile.zlib.DEFLATED)
	pre_len = len(os.path.dirname(source_dir))
	for parent, dirnames, filenames in os.walk(source_dir):
		for filename in filenames:
			pathfile = os.path.join(parent, filename)
			arcname = pathfile[pre_len:].strip(os.path.sep)
			zipf.write(pathfile, arcname)
	zipf.close()

class PackageforUpload_Imifun():
	def __init__(self,ftp_ip,ftp_port,ftp_user,ftp_passwd):
		self.ftp_ip = ftp_ip
		self.ftp_port = ftp_port
		self.ftp_user = ftp_user
		self.ftp_passwd = ftp_passwd
		# self.t = paramiko.Transport((self.ftp_ip,self.ftp_port))
		# self.t.connect(username=self.ftp_user,password=self.ftp_passwd)
		# self.sftp = paramiko.SFTPClient.from_transport(self.t)
		# self.ssh = paramiko.SSHClient()
		# self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# self.ssh.connect(ftp_ip,ftp_port,ftp_user,ftp_passwd)
		self.sftp = pysftp.Connection(host=ftp_ip,port=ftp_port,username=ftp_user,password=ftp_passwd)
	def putAndroidChannel(self,mysql_connect,channel_id,pkgname,localpath,remotepath):
		remotepath_apk = remotepath+pkgname
		localpath_apk = os.path.join(localpath,pkgname)
		remotepath_back_apk = remotepath+'apk_backup/'+pkgname
		try:
			self.sftp.rename(remotepath_apk,remotepath_back_apk)
		except Exception,e:
			# logger.debug(e)
			pass
		try:
			self.sftp.put(localpath_apk,remotepath_apk)
			mysql_connect.setPackageUploadStatus(channel_id,2)
		except Exception,e:
			# logger.error(e)
			mysql_connect.setPackageUploadStatus(channel_id,3)


class PackageforUpload_Yunfan():
	def __init__(self,ftp_ip,ftp_port,ftp_user,ftp_passwd):
		self.ftp_ip = ftp_ip
		self.ftp_port = ftp_port
		self.ftp_user = ftp_user
		self.ftp_passwd = ftp_passwd
		self.ftp = ftplib.FTP()
		self.ftp.connect(ftp_ip,ftp_port)
		self.ftp.login(ftp_user,ftp_passwd)
	def putAndroidChannel(self,mysql_connect,channel_id,pkgname,localpath,remotepath):
		localpath_apk = os.path.join(localpath,pkgname)
		remotepath_apk = remotepath+pkgname
		remotepath_back_apk = remotepath+'apk_backup/'+pkgname
		fp=open(localpath_apk,'rb')
		try:
			self.ftp.delete(remotepath_back_apk)
		except:pass
		try:
			self.ftp.rename(remotepath_apk,remotepath_back_apk)
		except Exception,e:
			pass
			# logger.error(e)
		try:
			self.ftp.cwd(remotepath)
			self.ftp.storbinary("STOR %s" %pkgname,fp)
			mysql_connect.setPackageUploadStatus(channel_id,2)
		except Exception,e:
			# logger.error(e)
			mysql_connect.setPackageUploadStatus(channel_id,3)
	def closeFtp(self):
		self.ftp.close()

class MyThreadForUploadPackage_Imifun(threading.Thread):
	def __init__(self,idForup,ftp_ip,ftp_port,ftp_user,ftp_passwd,channel_id,package_name,platform,channel,localpath,remotepath):
		threading.Thread.__init__(self)
		self.idForup = idForup
		self.ftp_ip = ftp_ip
		self.ftp_port = ftp_port
		self.ftp_user = ftp_user
		self.ftp_passwd = ftp_passwd
		self.channel_id = channel_id
		self.package_name = package_name
		self.platform = platform
		self.channel = channel
		self.localpath = localpath
		self.remotepath = remotepath
		self.mysql_connect=Mysql_for_AndroidChannel()
	def run(self):
		try:
			if self.channel==8000 or self.channel==7999:
				ApkUp = PackageforUpload_Imifun(self.ftp_ip,self.ftp_port,self.ftp_user,self.ftp_passwd)
				ApkUp.putAndroidChannel(self.mysql_connect,self.channel_id,self.package_name,self.localpath,self.remotepath)
			else:
				ApkUp = PackageforUpload_Imifun(self.ftp_ip,self.ftp_port,self.ftp_user,self.ftp_passwd)
				while self.mysql_connect.getChannel_uploadSum(self.platform):
					channel = self.mysql_connect.getChannel_upload(self.platform)
					ApkUp.putAndroidChannel(self.mysql_connect,channel.id,channel.package_name,self.localpath,self.remotepath)
		except Exception,e:
			logging.error(e)
			while self.mysql_connect.getChannel_uploadSum(self.platform):
				channel = self.mysql_connect.getChannel_upload(self.platform)
				self.mysql_connect.setPackageUploadStatus(channel.id,3)
		finally:self.mysql_connect.session_close()

class MyThreadForUploadPackage_Yunfan(threading.Thread):
	def __init__(self,ftp_ip,ftp_port,ftp_user,ftp_passwd,platform,localpath,remotepath):
		threading.Thread.__init__(self)
		self.ftp_ip = ftp_ip
		self.ftp_port = ftp_port
		self.ftp_user = ftp_user
		self.ftp_passwd = ftp_passwd
		self.platform = platform
		self.localpath = localpath
		self.remotepath = remotepath
		self.mysql_connect=Mysql_for_AndroidChannel()
	def run(self):
		try:
			ApkUp = PackageforUpload_Yunfan(self.ftp_ip,self.ftp_port,self.ftp_user,self.ftp_passwd)
			while self.mysql_connect.getChannel_uploadSum_Yunfan(self.platform):
				channel = self.mysql_connect.getChannel_upload_Yunfan(self.platform)
				ApkUp.putAndroidChannel(self.mysql_connect,channel.id,channel.package_name,self.localpath,self.remotepath)
			ApkUp.closeFtp()
		except Exception,e:
			# logger.error(e)
			while self.mysql_connect.getChannel_uploadSum(self.platform):
				channel = self.mysql_connect.getChannel_upload(self.platform)
				self.mysql_connect.setPackageUploadStatus(channel.id,3)
		finally:self.mysql_connect.session_close()


def uploadPackage_Imifun(idForup,ftp_ip,ftp_port,ftp_user,ftp_passwd,channel_id,package_name,platform,channel,localpath,remotepath):
	thr = MyThreadForUploadPackage_Imifun(idForup,ftp_ip,ftp_port,ftp_user,ftp_passwd,channel_id,package_name,platform,channel,localpath,remotepath)
	thr.start()
	return thr

def uploadPackage_Yunfan(ftp_ip,ftp_port,ftp_user,ftp_passwd,platform,localpath,remotepath):
	thr = MyThreadForUploadPackage_Yunfan(ftp_ip,ftp_port,ftp_user,ftp_passwd,platform,localpath,remotepath)
	thr.start()
	return thr


