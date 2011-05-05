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
    def get_item(self, item_id, basic=False, **kwargs):
        '''
        Get item

        Arguments:
            item_id: Item's id
        Returns:
            Dict with item info
        '''
        if basic:
            return self.transport.GET(url = "/item/%r/basic" % item_id)
        return self.transport.GET(kwargs, url = "/item/%r" % item_id)

    def next_item(self, item_id, **kwargs):
        return self.transport.GET(url = "/item/%r/next" % item_id)
    
    def prev_item(self, item_id, **kwargs):
        return self.transport.GET(url = "/item/%r/previous" % item_id)

class Applications(Area):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
    def activate_app(self, app_id):
        '''
        Activates the application with app_id
          
          Arguments:
            app_id: Application ID as string or int
          Returns:
            Python dict of JSON response
        '''
        return self.transport.POST(url = "/app/%r/activate" % app_id)
        
    def deactivate_app(self, app_id):
        '''
        Deactivates the application with app_id
          
          Arguments:
            app_id: Application ID as string or int
          Returns:
            Python dict of JSON response
        '''
        return self.transport.POST(url = "/app/%r/deactivate" % app_id)
    
    def delete_app(self, app_id):
        '''
        Deletes the app with the given id.
        
            Arguments:
              app_id: Application ID as string or int
        '''
        return self.transport.DELETE(url="/app/%r" % app_id)
    
    def find(self, app_id):
        '''
        Finds application with id app_id.

          Arguments:
            app_id: Application ID as string or int
          Returns:
            Python dict of JSON response
        '''
        return self.transport.GET(url = "/app/%r" % app_id)
    
    def list_apps_in_space(self, space_id):
        '''
        Returns a list of all the visible apps in a space.

          Arguemtns:
            space_id: Space ID as a string
        '''
        return self.transport.GET(url = "/app/space/%r/" % space_id)

    def get_items(self, app_id, **kwargs):
        return self.transport.GET(url = "/item/app/%r/" % app_id, **kwargs)

class Tasks(Area):
    def __init__(self, *args, **kwargs):
        super(Tasks, self).__init__(*args, **kwargs)
    
    def get_tasks(self, **kwargs):
        '''
        Get tasks endpoint. QueryStrings are kwargs
        '''
        return self.transport.GET('/task/', **kwargs)
    
            
    def delete_task(self, task_id):
        '''
        Deletes the app with the given id.
        Arguments:
        task_id: Task ID as string or int
        '''
        return self.transport.DELETE(url="/task/%r" % task_id)
            
    def complete_task(self, task_id):
        '''
        Mark the given task as completed.
        Arguments:
            task_id: Task ID as string or int
        '''
        return self.transport.POST(url = "/task/%r/complete" % task_id)

class Users(Area):
    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
    
class Spaces(Area):
    def __init__(self, *args, **kwargs):
        super(Spaces, self).__init__(*args, **kwargs)
    
    def find_by_url(self, space_url, id_only=True):
        '''
        Returns a space ID given the URL of the space.

          Arguments:
            space_url: URL of the Space
          
          Returns:
            space_id: Space url as string
        '''        
        resp = self.transport.GET(url = "/space/url?%r" % urllib.urlencode(dict(url=space_url)))
        if id_only:
            return resp['space_id']
        return resp
    
    def find_all_for_org(self, org_id):
        '''
        Find all of the spaces in a given org.
          
          Arguments:
            org_id: Orginization ID as string
          returns:
            Dict containing details of spaces
        '''
        return self.transport.GET(url = "/org/%r/space/" % org_id)
    
    def create(self, attributes):
        '''
        Create a new space
          Arguments:
            Refer to API. Pass in argument as dictionary
          returns:
            Dict containing details of newly created space
        '''
        if type(attributes) != dict:
            raise ApiErrorException("Dictionary of values expected")
        attributes = json.dumps(attributes)
        return self.transport.POST(
            url = "/space/", 
            body = attributes, 
            type = 'application/json'
        )
        