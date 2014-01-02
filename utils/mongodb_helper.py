from pymongo import MongoClient

class MDB:
	def __init__(self, config):
		self.config = config
		client = MongoClient(config['host'],config['port'])
		db = client[config['db']]
		self.db = db
		doc = db[config['doc']]
		self.doc = doc
	def insert(self, data):
		return self.doc.insert(data)
	def search(self, condition):
		return self.doc.find(condition)
	def update():
		pass
	def delete():
		pass
