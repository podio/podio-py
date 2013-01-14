try:
    import json
except ImportError:
    import simplejson as json
from urllib import urlencode


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
            return self.transport.GET(url='/item/%d/basic' % item_id)
        return self.transport.GET(kwargs, url='/item/%d' % item_id)

    def filter(self, app_id, attributes):
        if type(attributes) != dict:
            return ApiErrorException('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url="/item/app/%d/filter/" % app_id, body=attributes, type="application/json")

    def next(self, item_id, **kwargs):
        return self.transport.GET(url='/item/%d/next' % item_id)

    def prev(self, item_id, **kwargs):
        return self.transport.GET(url='/item/%d/previous' % item_id)

    def find_all_by_external_id(self, app_id, external_id):
        return self.transport.GET(url='/item/app/%d/v2/?external_id=%r' % (app_id, external_id))

    def revisions(self, item_id):
        return self.transport.GET(url='/item/%d/revision/' % item_id)

    def revision_difference(self, item_id, revision_from_id, revision_to_id):
        return self.transport.GET(url='/item/%d/revision/%d/%d' % (item_id, revision_from_id, revision_to_id))

    def create(self, app_id, attributes):
        if type(attributes) != dict:
            return ApiErrorException('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/item/app/%d/' % app_id, body=attributes,
                                   type='application/json')

    def update(self, item_id, attributes, silent=False):
        """Updates the item using the supplied attributes. If 'silent' is true, Podio will send
        no notifications to subscribed users and not post updates to the stream.
        Important: webhooks ll still be called, though."""
        if type(attributes) != dict:
            return ApiErrorException('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.PUT(url='/item/%d%s' % (item_id, "?silent=true" if silent else ""), body=attributes,
                                   type='application/json')

    def delete(self, item_id):
        return self.transport.DELETE(url='/item/%d' % item_id, handler=lambda x, y: None)


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
        return self.transport.POST(url='/app/%s/activate' % app_id)

    def create(self, attributes):
        if type(attributes) != dict:
            return ApiErrorException('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/app/', body=attributes, type='application/json')

    def deactivate(self, app_id):
        '''
        Deactivates the application with app_id
          
          Arguments:
            app_id: Application ID as string or int
          Returns:
            Python dict of JSON response
        '''
        return self.transport.POST(url='/app/%s/deactivate' % app_id)

    def delete(self, app_id):
        '''
        Deletes the app with the given id.
        
            Arguments:
              app_id: Application ID as string or int
        '''
        return self.transport.DELETE(url='/app/%s' % app_id)

    def find(self, app_id):
        '''
        Finds application with id app_id.

          Arguments:
            app_id: Application ID as string or int
          Returns:
            Python dict of JSON response
        '''
        return self.transport.GET(url='/app/%s' % app_id)

    def get_items(self, app_id, **kwargs):
        return self.transport.GET(url='/item/app/%s/' % app_id, **kwargs)

    def list_in_space(self, space_id):
        '''
        Returns a list of all the visible apps in a space.

          Arguemtns:
            space_id: Space ID as a string
        '''
        return self.transport.GET(url='/app/space/%s/' % space_id)


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
        return self.transport.DELETE(url='/task/%s' % task_id)

    def complete(self, task_id):
        '''
        Mark the given task as completed.
        Arguments:
            task_id: Task ID as string or int
        '''
        return self.transport.POST(url='/task/%s/complete' % task_id)


class User(Area):

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def current(self):
        return self.transport.get(url='/user/')

class Org(Area):

    def __init__(self, *args, **kwargs):
        super(Org, self).__init__(*args, **kwargs)

    def get_all(self):
        return self.transport.get(url='/org/')


class Status(Area):

    def __init__(self, *args, **kwargs):
        super(Status, self).__init__(*args, **kwargs)

    def find(self, status_id):
        return self.transport.GET(url='/status/%s' % status_id)

    def create(self, space_id, attributes):
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/status/space/%s/' % space_id,
                                   body=attributes, type='application/json')


class Space(Area):

    def __init__(self, *args, **kwargs):
        super(Space, self).__init__(*args, **kwargs)

    def find(self, space_id):
        return self.transport.GET(url='/space/%s' % id)

    def find_by_url(self, space_url, id_only=True):
        '''
        Returns a space ID given the URL of the space.

          Arguments:
            space_url: URL of the Space
          
          Returns:
            space_id: Space url as string
        '''
        resp = self.transport.GET(url='/space/url?%s' % urlencode(dict(url=space_url)))
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
        return self.transport.GET(url='/org/%s/space/' % org_id)

    def create(self, attributes):
        '''
        Create a new space
          Arguments:
            Refer to API. Pass in argument as dictionary
          returns:
            Dict containing details of newly created space
        '''
        if type(attributes) != dict:
            raise ApiErrorException('Dictionary of values expected')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/space/', body=attributes,
                                   type='application/json')

class Stream(Area):
    """
    The stream API will supply the different streams. Currently
    supported is the global stream, the organization stream and the
    space stream.

    For details, see: https://developers.podio.com/doc/stream/
    """
    def find_all_by_app_id(self, app_id):
        """
        Returns the stream for the given app. This includes items from
        the app and tasks on the app.

        For details, see: https://developers.podio.com/doc/stream/get-app-stream-264673
        """
        return self.transport.GET(url='/stream/app/%s/' % app_id)

    def find_all(self):
        """
        Returns the global stream. The types of objects in the stream
        can be either "item", "status", "task", "action" or
        "file". The data part of the result depends on the type of
        object and is specified on this page:

        https://developers.podio.com/doc/stream/get-global-stream-80012
        """
        return self.transport.GET(url='/stream/')

    def find_all_by_org_id(self, org_id):
        """
        Returns the activity stream for the given organization.

        For details, see: https://developers.podio.com/doc/stream/get-organization-stream-80038
        """
        return self.transport.GET(url='/stream/org/%s/' % org_id)

    def find_all_personal(self):
        """
        Returns the personal stream from personal spaces and sub-orgs.

        For details, see: https://developers.podio.com/doc/stream/get-personal-stream-1656647
        """
        return self.transport.GET(url='/stream/personal/')

    def find_all_by_space_id(self, space_id):
        """
        Returns the activity stream for the space.

        For details, see: https://developers.podio.com/doc/stream/get-space-stream-80039
        """
        return self.transport.GET(url='/stream/space/%s/' % space_id)

    def find_by_ref(self, ref_type, ref_id):
        """
        Returns an object of type "item", "status" or "task" as a
        stream object. This is useful when a new status has been
        posted and should be rendered directly in the stream without
        reloading the entire stream.

        For details, see: https://developers.podio.com/doc/stream/get-stream-object-80054
        """
        return self.transport.GET(url='/stream/%s/%s' % (ref_type, ref_id))


class Hook(Area):

    def __init__(self, *args, **kwargs):
        super(Hook, self).__init__(*args, **kwargs)

    def create(self, hookable_type, hookable_id, attributes):
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/hook/%s/%s/' % (hookable_type, hookable_id),
                                   body=attributes, type='application/json')

    def verify(self, hook_id):
        return self.transport.POST(url='/hook/%s/verify/request' % hook_id)

    def validate(self, hook_id, code):
        return self.transport.POST(url='/hook/%s/verify/validate' % hook_id,
                                   code=code)

    def delete(self, hook_id):
        return self.transport.DELETE (url='/hook/%s' % hook_id)

    def find_all_for(self, hookable_type, hookable_id):
        return self.transport.GET(url='/hook/%s/%s/' % (hookable_type, hookable_id))


class Connection(Area):

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)

    def create(self, attributes):
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/connection/', body=attributes,
                                   type='application/json')

    def find(self, conn_id):
        return self.transport.GET(url='/connection/%s')

    def delete(self, conn_id):
        return self.transport.DELETE(url='/connection/%s')

    def reload(self, conn_id):
        return self.transport.POST(url='/connection/%s/load')


class Notification(Area):

    def __init__(self, *args, **kwargs):
        super(Notification, self).__init__(*args, **kwargs)

    def find(self, notification_id):
        return self.transport.GET(url='/notification/%s' % notification_id)

    def mark_as_viewed(self, notification_id):
        return self.transport.POST(url='/notification/%s/viewed' % notification_id)

    def mark_all_as_viewed(self):
        return self.transport.POST(url='/notification/viewed')

    def star(self, notification_id):
        return self.transport.POST(url='/notification/%s/star' % notification_id)

    def unstar(self, notification_id):
        return self.transport.POST(url='/notification/%s/star' % notification_id)


class Files(Area):

    def __init__(self, *args, **kwargs):
        super(Files, self).__init__(*args, **kwargs)

    def find(self, file_id):
        pass

    def find_raw(self, file_id):
        '''Returns raw file as string. Pass to a file object'''
        raw_handler = lambda resp, data: data
        return self.transport.GET(url='/file/%d/raw' % file_id, handler=raw_handler)
        
    def attach(self, file_id, ref_type, ref_id):
        attributes = {
            'ref_type' : ref_type,
            'ref_id' : ref_id
        }
        return self.transport.POST(url='/file/%s/attach' % (file_id,), body=json.dumps(attributes), type='application/json')

    def create(self, filename, filedata):
        '''Create a file from raw data'''
        attributes = {
            'filename' : filename,
            'source' : filedata
        }
        
        return self.transport.POST(url='/file/v2/', body=attributes,
                                   type='multipart/form-data')