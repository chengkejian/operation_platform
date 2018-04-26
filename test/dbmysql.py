#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: dbmysql.py
@time: 2016/9/23 14:17
"""

from sqlalchemy import create_engine, text, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Product(Base):
	__tablename__='products'
	id = Column(Integer,Sequence('id'),primary_key=True)
	name = Column(String(8))
	count = Column(Integer)


	def __repr__(self):
		return "Product<id= %d ,name = %s ,count= %d >" %(self.id,self.name,self.count)

DB_URL = 'mysql://root:centos@10.10.10.103:3306/test?charset=utf8'
engine = create_engine(DB_URL,echo=False)
Session = sessionmaker(bind=engine)
session = Session()
# Base.metadata.create_all(engine)
# pro = Product(id=1,name='ckj',count=20)
# prd = Product(id=2,name='xjw',count=120)
# ppp = Product(id=4,name='love',count=43)
#
# session.add_all([ppp]).filter_by(name='love').all()
# session.commit()
product = session.query(Product).first()

print product
print(type(product))






















