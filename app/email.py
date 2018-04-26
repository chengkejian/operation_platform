#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: email.py
@time: 2016/8/30 16:12
"""
from threading import Thread
from flask_mail import Message
from flask import render_template,current_app
from . import mail

def send_async_email(app,msg):
	with app.app_context():
		mail.send(msg)
def send_email(to,subject,templete,**kwargs):
	app = current_app._get_current_object()
	msg = Message(app.config['MOBIM_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['MOBIM_MAIL_SENDER'],
				  recipients=[to])
	# msg.body = render_template(templete+'.txt',**kwargs)
	msg.body = render_template(templete+'.txt',**kwargs)
	msg.html = render_template(templete+'.html',**kwargs)
	thr = Thread(target=send_async_email,args=[app,msg])
	thr.start()
	return thr