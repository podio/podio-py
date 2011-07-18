class Object(object):
	def __init__(self,client,**kw):
		self.client = client
		self.kw = kw
		
	ptype = ''
	
	def __repr__(self):
		return '<Podio %s id=%d>' % (self.ptype, self.id)
	
	@property
	def id(self):
		return self.kw[self.ptype + '_id']

	def add_comment(self, text):
		"""
		Add a comment to object
		"""
		return Comment.add_to(self, text)
		
	@property
	def comments(self):
		"""
		Get all comments to this object.
		(Shadows the 'comments' field)
		"""
		cs = self.client.transport.GET(
						url='/comment/%s/%r/' % (self.ptype, self.id))
		return [Comment(self.client,**useAsciiKeys(c)) for c in cs]
			
		
	def create(self,**kw):
		import json
		attrs = json.dumps(kw)
		return self.client.transport.POST(
			url = '/%s/'%self.ptype,
			body= attrs,
			type='application/json')
			
	def destroy(self):
		self.client.transport.DELETE(
			url='/%s/%r'%(self.ptype,self.id))
			
class Comment(Object):
	ptype = 'comment'
	
	@property
	def text(self):
		return self.kw['value']
		
	def __str__(self):
		return self.text
	
	@classmethod
	def add_to(klass,pobj,text):
		import json
		tp = pobj.ptype
		attrs = dict(value=text)
		response = pobj.client.transport.POST(
				url= '/comment/%s/%r/' % (tp,pobj.id),
				body= json.dumps(attrs),
				type= 'application/json')
		return Comment(pobj.client, **useAsciiKeys(response))
		
			
class Space(Object):
	ptype = 'space'
			
class Notification(Object):
	ptype = 'notification'
	
	star = lambda s: s.post('star')
	


				
class Item(Object):
	ptype = 'item'
	
	def __iter__(self):
		return self
		
	def check(self):
		"""
		Is it conformant?
		"""
		if self.kw.has_key('fields'):
			return bool(self.kw['fields'])
		else:
			return False
		
	@classmethod
	def fromPodio(klass,client,item_id):
		kw = client.Item.find(item_id)
		return Item(client,**useAsciiKeys(kw))
		
	def __getattr__(self,k):
		if self.kw.has_key(k):
			return self.kw[k]
		else:
			raise AttributeError
			
	def __getitem__(self,k):
		fd = self.get_field(k)
		if fd:
			return fd
		else:
			raise KeyError
			
	def get_field(self,k):
		for f in self.kw['fields']:
			if k == f['external_id']: return f['values']
		return None
		
	@property	
	def keys(self):
		return [f['external_id'] for f in self.kw['fields']]
		
	def next(self):
		try:
			Item(self.transport,**self.get('next'))
		except:
			raise StopIteration
			
			
class Application(Object):
	ptype ='app'
	itemclass = Item

	activate = lambda s: s.post('activate')
	deactivate = lambda s: s.post('deactivate')

	@classmethod
	def fromPodio(klass,client,app_id):
		app = client.Application.find(app_id)
		return Application(client, **useAsciiKeys(app))

	@property
	def items(self):
		items = self.client.Application.get_items(self.id)['items']
		return [Item.fromPodio(self.client,i['item_id']) for i in items]


	def add_item(self,**fields):
		pfields = {'fields': [simpleField(k,v) for k,v in fields.items()]}
		item = self.client.Item.create(self.id, pfields)
		#nitem = super(Item, self.itemclass).__new__(self.itemclass, self.client,item)
		#return Item(self.client,**item['fields'])
		return item
			

# Utils
			
def useAsciiKeys(d):
	return dict([(str(k),v) for k,v in d.items()])
	
def simpleField(k,v):
	"""
	Just 1 value (v) for key k
	"""
	return 	{"external_id":k, "values":[{"value":v}]}
			

if __name__ == '__main__':
	from mydata import config 
	from pypodio2 import api
	client_data = [config[k] for k in 'client_id client_secret username password'.split()]
	c = api.OAuthClient(*client_data)
	
	app = Application.fromPodio(c, config['app_id'])
	for i in app.items:
		print i.title, i.get_field('date')
		i.add_comment("No comment")
		for c in i.comments:
			print "Comment:", c
		
	
