class Area(object):
    'Represents a Podio Area'
    def __init__(self, transport, *args, **kwargs):
        self.transport = transport
    def sanitize_id(self, item_id):
        if(type(item_id) == int):
            return str(item_id)
        return item_id

class Items(Area):
    def __init__(self, *args, **kwargs):
        super(Items, self).__init__(*args, **kwargs)
    def get_item(self, item_id, **kwargs):
        item_id=self.sanitize_id(item_id)
        return self.transport.GET(kwargs, url='/item/%s' % item_id)

class Application(Area):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

class Tasks(Area):
    def __init__(self, *args, **kwargs):
        super(Tasks, self).__init__(*args, **kwargs)

class Users(Area):
    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
           