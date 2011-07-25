import json
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
		
	def add_tags(self,*texts):
		"""
		Add tags to the object
		"""
		attrs = json.dumps([s.encode('utf8') for s in texts])
		self.client.transport.POST(
			url='/tag/%s/%r/' % (self.ptype,self.id),
			body=attrs,
			type='application/json')
			
		
	def create(self,**kw):
		attrs = json.dumps(kw)
		return self.client.transport.POST(
			url = '/%s/'%self.ptype,
			body= attrs,
			type='application/json')
			
	def destroy(self):
		self.client.transport.DELETE(
			url='/%s/%r'%(self.ptype,self.id))
			
class User(Object):
	ptype = 'user'
	
	def __str__(self):
		return self.kw['name']
		
	@classmethod
	def current(klass,client):
		profile = client.transport.GET(url='/%s/profile/' % klass.ptype)
		return User(client,**useAsciiKeys(profile))
		
	def __getattr__(self,k):
		if self.kw.has_key(k):
			return self.kw[k]
		else:
			raise AttributeError, "Not found in Podio dict: %s" % k
	
			
class Comment(Object):
	ptype = 'comment'
	
	@property
	def text(self):
		return self.kw['value']
		
	def __str__(self):
		return self.text
	
	@classmethod
	def add_to(klass,pobj,text):
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
		return klass(client,**useAsciiKeys(kw))
		
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
		
	def set_field(self,k,v):
		self.kw['fields'][k] = [aValue(v)]
		
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
		return klass(client, **useAsciiKeys(app))

	@property
	def items(self):
		items = self.client.Application.get_items(self.id)['items']
		return [self.itemclass.fromPodio(self.client,i['item_id']) for i in items]


	def add_item(self,**fields):
		pfields = {'fields': [simpleField(k,v) for k,v in fields.items()]}
		fields = self.client.Item.create(self.id, pfields)
		#nitem = super(Item, self.itemclass).__new__(self.itemclass, self.client,item)
		#return Item(self.client,**item['fields'])
		return Item(self.client,**useAsciiKeys(fields))
			

# Utils
			
def useAsciiKeys(d):
	return dict([(str(k),v) for k,v in d.items()])
	
def aValue(v):
	return {'value': v}
	
def simpleField(k,v):
	"""
	Just 1 value (v) for key k
	"""
	return 	{"external_id":k, "values":[aValue(v)]}
			

if __name__ == '__main__':
	from mydata import config
	from pypodio2 import api
	client_data = [config[k] for k in 'client_id client_secret username password'.split()]
	client = api.OAuthClient(*client_data)
	
	app = Application.fromPodio(client, config['app_id'])
	for i in app.items:
		print i.title, i.get_field('date')
		#i.add_comment("No comment")
		for cm in i.comments:
			print "Comment:", cm
	import pdb
	user = User.current(client)
		
	
