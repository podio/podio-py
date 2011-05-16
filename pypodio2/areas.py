import json
class Area(object):
    'Represents a Podio Area'
    def __init__(self, transport, *args, **kwargs):
        self.transport = transport
    def sanitize_id(self, item_id):
        if(type(item_id) == int):
            return str(item_id)
        return item_id

class Item(Area):
    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
    def find(self, item_id, basic=False, **kwargs):
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

    def next(self, item_id, **kwargs):
        return self.transport.GET(url = "/item/%r/next" % item_id)
    
    def prev(self, item_id, **kwargs):
        return self.transport.GET(url = "/item/%r/previous" % item_id)
    
    def find_all_by_external_id(self, app_id, external_id):
        return self.transport.GET(url = "/item/app/%r/v2/?external_id=%r" % (app_id, external_id))
    
    def revisions(self, item_id):
        return self.transport.GET(url = "/item/%r/revision/" % item_id)
    
    def revision_difference(self, item_id, revision_from_id, revision_to_id):
        return self.transport.GET(url = "/item/%r/revision/%r/%r" % (item_id, revision_from_id, revision_to_id))
    
    def create(self, app_id, attributes):
        if type(attributes) != dict:
            return ApiErrorException("Must be of type dict")
        attributes = json.dumps(attributes)
        
        return self.transport.POST(
            url = "/item/app/%d/" % app_id,
            body = attributes,
            type = 'application/json'
    )

class Application(Area):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
    def activate(self, app_id):
        '''
        Activates the application with app_id
          
          Arguments:
            app_id: Application ID as string or int
          Returns:
            Python dict of JSON response
        '''
        return self.transport.POST(url = "/app/%r/activate" % app_id)
    
    def create(self, attributes):
        if type(attributes) != dict:
            return ApiErrorException("Must be of type dict")
        attributes = json.dumps(attributes)

        return self.transport.POST(
            url = "/app/", 
            body = attributes,
            type = 'application/json'
        )


    def deactivate(self, app_id):
        '''
        Deactivates the application with app_id
          
          Arguments:
            app_id: Application ID as string or int
          Returns:
            Python dict of JSON response
        '''
        return self.transport.POST(url = "/app/%r/deactivate" % app_id)
    
    def delete(self, app_id):
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
    
    def get_items(self, app_id, **kwargs):
        return self.transport.GET(url = "/item/app/%r/" % app_id, **kwargs)

    def list_in_space(self, space_id):
        '''
        Returns a list of all the visible apps in a space.

          Arguemtns:
            space_id: Space ID as a string
        '''
        return self.transport.GET(url = "/app/space/%r/" % space_id)

class Task(Area):
    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
    
    def get(self, **kwargs):
        '''
        Get tasks endpoint. QueryStrings are kwargs
        '''
        return self.transport.GET('/task/', **kwargs)
    
            
    def delete(self, task_id):
        '''
        Deletes the app with the given id.
        Arguments:
        task_id: Task ID as string or int
        '''
        return self.transport.DELETE(url="/task/%r" % task_id)
            
    def complete(self, task_id):
        '''
        Mark the given task as completed.
        Arguments:
            task_id: Task ID as string or int
        '''
        return self.transport.POST(url = "/task/%r/complete" % task_id)

class User(Area):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
    
class Space(Area):
    def __init__(self, *args, **kwargs):
        super(Space, self).__init__(*args, **kwargs)
    
    def find(self, space_id):
        return self.transport.GET(url = '/space/%r' % id)
    
    def find_by_url(self, space_url, id_only=True):
        '''
        Returns a space ID given the URL of the space.

          Arguments:
            space_url: URL of the Space
          
          Returns:
            space_id: Space url as string
        '''        
        from urllib import urlencode
        
        resp = self.transport.GET(url = "/space/url?%s" % urlencode(dict(url=space_url)))
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

class Hook(Area):
    def __init__(self, *args, **kwargs):
        super(Hook, self).__init__(*args, **kwargs)
    
    def create(self, hookable_type, hookable_id, attributes):
        attributes = json.dumps(attributes)
        return self.transport.POST(
            url = '/hook/%r/%r/' % (hookable_type, hookable_id),
            body = attributes
            type = 'application/json'
        )
    def verify(self, hook_id):
        return self.transport.POST(url = '/hook/%r/verify/request' % hook_id)

    def validate(self, hook_id, code):
        return self.transport.POST(
            url = '/hook/%r/verify/validate' % hook_id,
            code = code
        )

    def delete(self, hook_id):
        return self.transport.DELETE (url = '/hook/%r' % hook_id)
    
    def find_all_for(self, hookable_type, hookable_id):
        return self.transport.GET(
            url = '/hook/%r/%r/' % (hookable_type, hookable_id)
        )

# class File(Area):
#     """Files area"""
#     def __init__(self, *args, **kwargs):
#         super(File, self).__init__(*args, **kwargs)
      
#     def set_available(id):
#         return self.transport.POST(url = "/file/%r/available" % id)
    
#     def attach(self, id, ref_type, ref_id):
#         pass