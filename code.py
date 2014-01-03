#! /usr/bin/env python
#coding=utf-8

import web
from mako.template import Template
from mako.lookup import TemplateLookup
from utils.mongodb_helper import MDB
import random
from bson.objectid import ObjectId

urls = (
		'/', 'GetARandomLetter',
		'/getaramdomletter', 'GetARandomLetter',
		'/allletters/(.*)','AllLettersByPage',
		'/allletters','AllLettersByPage',
		'/letter/(.*)','ViewALetter'
)

#全局变量
tem_lookup = TemplateLookup(directories=['templates'],input_encoding='utf-8',output_encoding='utf-8',default_filters=['h', 'decode.utf8'])
mdbconfig = {'host':'localhost','port':27017,'db':'w','doc':'letter'}

class Index:
	def GET(self):
		tem = tem_lookup.get_template('/index.html')
		return tem.render()

#随机文章显示页面
class GetARandomLetter:
	def GET(self):
		tem = tem_lookup.get_template('/fun/aletter.html')
		mdb = MDB(mdbconfig)
		rd = random.random()
		letterA = mdb.doc.find({"rd":{"$gt":rd}}).sort("rd").limit(1)
		letterA = letterA[0] if letterA.count() > 0 else {}
		letterB = mdb.doc.find({"rd":{"$lt":rd}}).sort("rd", -1).limit(1)
		letterB = letterB[0] if letterB.count() > 0 else {}
		letters = letterB if letterA == {} or (letterB <> {} and letterA['rd'] - rd > letterB['rd'] - rd) else letterA
		return tem.render(letter=letters, rd=rd)

#所有文章显示列表
class AllLettersByPage:
	def GET(slef, page):
		#每页数目
		limit = 10
		if not page:
			#默认初始页
			page = 1
		page = int(page)
		tem = tem_lookup.get_template('/fun/allletters.html')
		mdb = MDB(mdbconfig)
		total = mdb.doc.find().count()
		letters = mdb.doc.find().sort('date').skip((page-1)*limit).limit(limit)
		return tem.render(letters=letters, page=page, total=total, limit=limit)

#某篇具体文章
class ViewALetter:
	def GET(self, lid):
		tem = tem_lookup.get_template('/fun/aletter.html')
		mdb = MDB(mdbconfig)
		letter = mdb.doc.find_one({"_id":ObjectId(lid)})
		return tem.render(letter=letter)


if __name__ == '__main__':
	app = web.application(urls, globals())
	app.run()
