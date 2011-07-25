import objects
from objects import useAsciiKeys

class Timesheet(objects.Item):
	@property
	def deliverable(self):
		field = self['deliverable-worked-on']
		assert len(field) == 1
		return Deliverable(self.client,**useAsciiKeys(field[0]['value']))

	@property
	def employee(self):
		field = self['employee']
		assert len(field) == 1
		return objects.User(self.client,**useAsciiKeys(field[0]['value']))
				

class Deliverable(objects.Item):
	pass
	
class Timesheets(objects.Application):
	itemclass = Timesheet
