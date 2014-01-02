import web
from mako.template import Template
from mako.lookup import TemplateLookup
from utils.mongodb_helper import MDB
import random

urls = (
		'/', 'GetARandomLetter',
		'/getaramdomletter', 'GetARandomLetter'
)

tem_lookup = TemplateLookup(directories=['templates'], output_encoding='utf-8', default_filters=['h', 'decode.utf8'])

class Index:
	def GET(self):
		tem = tem_lookup.get_template('/index.html')
		return tem.render()

class GetARandomLetter:
	def GET(self):
		tem = tem_lookup.get_template('/fun/aletter.html')
		mdb = MDB({'host':'localhost','port':27017,'db':'w','doc':'letter'})
		rd = random.random()
		letterA = mdb.doc.find({"rd":{"$gt":rd}}).sort("rd").limit(1)
		letterA = letterA[0] if letterA.count() > 0 else {}
		letterB = mdb.doc.find({"rd":{"$lt":rd}}).sort("rd", -1).limit(1)
		letterB = letterB[0] if letterB.count() > 0 else {}
		letters = letterB if letterA == {} or (letterB <> {} and letterA['rd'] - rd > letterB['rd'] - rd) else letterA
		return tem.render(letters=letters, rd=rd)

if __name__ == '__main__':
	app = web.application(urls, globals())
	app.run()
