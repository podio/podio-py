# -*- coding: utf-8 -*-
import json

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Area(object):
    """Represents a Podio Area"""
    def __init__(self, transport):
        self.transport = transport

    @staticmethod
    def sanitize_id(item_id):
        if isinstance(item_id, int):
            return str(item_id)
        return item_id

    @staticmethod
    def get_options(silent=False, hook=True):
        """
        Generate a query string with the appropriate options.

        :param silent: If set to true, the object will not be bumped up in the stream and
                       notifications will not be generated.
        :type silent: bool
        :param hook: True if hooks should be executed for the change, false otherwise.
        :type hook: bool
        :return: The generated query string
        :rtype: str
        """
        options_ = {}
        if silent:
            options_['silent'] = silent
        if not hook:
            options_['hook'] = hook
        if options_:
            return '?' + urlencode(options_).lower()
        else:
            return ''


class Embed(Area):

    def __init__(self, *args, **kwargs):
        super(Embed, self).__init__(*args, **kwargs)

    def create(self, attributes):
        if type(attributes) != dict:
            return ApiErrorException('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/embed/', body=attributes, type='application/json')


class Contact(Area):

    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)

    def create(self, space_id, attributes):
        if type(attributes) != dict:
            return ApiErrorException('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/contact/space/%d/' % space_id, body=attributes, type='application/json')


class Search(Area):

    def __init__(self, *args, **kwargs):
        super(Search, self).__init__(*args, **kwargs)

    def searchApp(self, app_id, attributes):
        if type(attributes) != dict:
            return ApiErrorException('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/search/app/%d/' % app_id, body=attributes, type='application/json')


class Item(Area):
    def find(self, item_id, basic=False, **kwargs):
        """
        Get item
        
        :param item_id: Item ID
        :param basic: ?
        :type item_id: int
        :return: Item info
        :rtype: dict
        """
        if basic:
            return self.transport.GET(url='/item/%d/basic' % item_id)
        return self.transport.GET(kwargs, url='/item/%d' % item_id)

    def filter(self, app_id, attributes, **kwargs):
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url="/item/app/%d/filter/" % app_id, body=attributes,
                                   type="application/json", **kwargs)

    def filter_by_view(self, app_id, view_id):
        return self.transport.POST(url="/item/app/{}/filter/{}".format(app_id, view_id))

    def find_all_by_external_id(self, app_id, external_id):
        return self.transport.GET(url='/item/app/%d/v2/?external_id=%r' % (app_id, external_id))

    def revisions(self, item_id):
        return self.transport.GET(url='/item/%d/revision/' % item_id)

    def revision_difference(self, item_id, revision_from_id, revision_to_id):
        return self.transport.GET(url='/item/%d/revision/%d/%d' % (item_id, revision_from_id,
                                                                   revision_to_id))

    def values(self, item_id):
        return self.transport.GET(url='/item/%s/value' % item_id)

    def values_v2(self, item_id):
        return self.transport.GET(url='/item/%s/value/v2' % item_id)

    def create(self, app_id, attributes, silent=False, hook=True):
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(body=attributes,
                                   type='application/json',
                                   url='/item/app/%d/%s' % (app_id,
                                                            self.get_options(silent=silent,
                                                                             hook=hook)))

    def update(self, item_id, attributes, silent=False, hook=True):
        """
        Updates the item using the supplied attributes. If 'silent' is true, Podio will send
        no notifications to subscribed users and not post updates to the stream.
        
        Important: webhooks will still be called.
        """
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.PUT(body=attributes,
                                  type='application/json',
                                  url='/item/%d%s' % (item_id, self.get_options(silent=silent,
                                                                                hook=hook)))

    def delete(self, item_id, silent=False, hook=True):
        return self.transport.DELETE(url='/item/%d%s' % (item_id,
                                                         self.get_options(silent=silent,
                                                                          hook=hook)),
                                     handler=lambda x, y: None)


class Application(Area):
    def activate(self, app_id):
        """
        Activates the application with app_id

        :param app_id: Application ID
        :type app_id: str or int
        :return: Python dict of JSON response
        :rtype: dict
        """
        return self.transport.POST(url='/app/%s/activate' % app_id)

    def create(self, attributes):
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/app/', body=attributes, type='application/json')

    def add_field(self, app_id, attributes):
        """
        Adds a new field to app with app_id

        :param app_id: Application ID
        :type app_id: str or int
        :param attributes: Refer to API.
        :type attributes: dict
        :return: Python dict of JSON response
        :rtype: dict
        """
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/app/%s/field/' % app_id, body=attributes,
                                   type='application/json')

    def deactivate(self, app_id):
        """
        Deactivates the application with app_id

        :param app_id: Application ID
        :type app_id: str or int
        :return: Python dict of JSON response
        :rtype: dict
        """
        return self.transport.POST(url='/app/%s/deactivate' % app_id)

    def delete(self, app_id):
        """
        Deletes the app with the given id.

        :param app_id: Application ID
        :type app_id: str or int
        """
        return self.transport.DELETE(url='/app/%s' % app_id)

    def find(self, app_id):
        """
        Finds application with id app_id.

        :param app_id: Application ID
        :type app_id: str or int
        :return: Python dict of JSON response
        :rtype: dict
        """
        return self.transport.GET(url='/app/%s' % app_id)

    def dependencies(self, app_id):
        """
        Finds application dependencies for app with id app_id.

        :param app_id: Application ID
        :type app_id: str or int
        :return: Python dict of JSON response with the apps that the given app depends on.
        :rtype: dict
        """
        return self.transport.GET(url='/app/%s/dependencies/' % app_id)

    def get_items(self, app_id, **kwargs):
        return self.transport.GET(url='/item/app/%s/' % app_id, **kwargs)

    def list_in_space(self, space_id):
        """
        Returns a list of all the visible apps in a space.

        :param space_id: Space ID
        :type space_id: str
        """
        return self.transport.GET(url='/app/space/%s/' % space_id)


class Task(Area):
    def get(self, **kwargs):
        """
        Get tasks endpoint. QueryStrings are kwargs
        """
        return self.transport.GET('/task/', **kwargs)

    def delete(self, task_id):
        """
        Deletes the app with the given id.
        
        :param task_id: Task ID
        :type task_id: str or int
        """
        return self.transport.DELETE(url='/task/%s' % task_id)

    def complete(self, task_id):
        """
        Mark the given task as completed.

        :param task_id: Task ID
        :type task_id: str or int
        """
        return self.transport.POST(url='/task/%s/complete' % task_id)

    def create(self, attributes, silent=False, hook=True):
        """
        https://developers.podio.com/doc/tasks/create-task-22419
        Creates the task using the supplied attributes. If 'silent' is true,
        Podio will send no notifications to subscribed users and not post
        updates to the stream. If 'hook' is false webhooks will not be called.
        """
        # if not isinstance(attributes, dict):
        #    raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/task/%s' % self.get_options(silent=silent, hook=hook),
                                   body=attributes,
                                   type='application/json')

    def create_for(self, ref_type, ref_id, attributes, silent=False, hook=True):
        """
        https://developers.podio.com/doc/tasks/create-task-with-reference-22420
        If 'silent' is true, Podio will send no notifications and not post
        updates to the stream. If 'hook' is false webhooks will not be called.
        """
        # if not isinstance(attributes, dict):
        #    raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(body=attributes,
                                   type='application/json',
                                   url='/task/%s/%s/%s' % (ref_type, ref_id,
                                                           self.get_options(silent=silent,
                                                                            hook=hook)))


class User(Area):
    def current(self):
        return self.transport.get(url='/user/')


class Org(Area):
    def get_all(self):
        return self.transport.get(url='/org/')


class Status(Area):
    def find(self, status_id):
        return self.transport.GET(url='/status/%s' % status_id)

    def create(self, space_id, attributes):
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/status/space/%s/' % space_id,
                                   body=attributes, type='application/json')


class Space(Area):
    def find(self, space_id):
        return self.transport.GET(url='/space/%s' % space_id)

    def find_by_url(self, space_url, id_only=True):
        """
        Returns a space ID given the URL of the space.

        :param space_url: URL of the Space
        :param id_only: ?
        :return: space_id: Space url
        :rtype: str
        """
        resp = self.transport.GET(url='/space/url?%s' % urlencode({'url': space_url}))
        if id_only:
            return resp['space_id']
        return resp

    def find_all_for_org(self, org_id):
        """
        Find all of the spaces in a given org.

        :param org_id: Orginization ID
        :type org_id: str
        :return: Details of spaces
        :rtype: dict
        """
        return self.transport.GET(url='/org/%s/space/' % org_id)

    def create(self, attributes):
        """
        Create a new space
        
        :param attributes: Refer to API. Pass in argument as dictionary
        :type attributes: dict
        :return: Details of newly created space
        :rtype: dict
        """
        if not isinstance(attributes, dict):
            raise TypeError('Dictionary of values expected')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/space/', body=attributes, type='application/json')


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
    def create(self, hookable_type, hookable_id, attributes):
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/hook/%s/%s/' % (hookable_type, hookable_id),
                                   body=attributes, type='application/json')

    def verify(self, hook_id):
        return self.transport.POST(url='/hook/%s/verify/request' % hook_id)

    def validate(self, hook_id, code):
        return self.transport.POST(url='/hook/%s/verify/validate' % hook_id, code=code)

    def delete(self, hook_id):
        return self.transport.DELETE(url='/hook/%s' % hook_id)

    def find_all_for(self, hookable_type, hookable_id):
        return self.transport.GET(url='/hook/%s/%s/' % (hookable_type, hookable_id))


class Connection(Area):
    def create(self, attributes):
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/connection/', body=attributes, type='application/json')

    def find(self, conn_id):
        return self.transport.GET(url='/connection/%s' % conn_id)

    def delete(self, conn_id):
        return self.transport.DELETE(url='/connection/%s' % conn_id)

    def reload(self, conn_id):
        return self.transport.POST(url='/connection/%s/load' % conn_id)


class Notification(Area):
    def find(self, notification_id):
        return self.transport.GET(url='/notification/%s' % notification_id)

    def find_all(self):
        return self.transport.GET(url='/notification/')

    def get_inbox_new_count(self):
        return self.transport.GET(url='/notification/inbox/new/count')

    def mark_as_viewed(self, notification_id):
        return self.transport.POST(url='/notification/%s/viewed' % notification_id)

    def mark_all_as_viewed(self):
        return self.transport.POST(url='/notification/viewed')

    def star(self, notification_id):
        return self.transport.POST(url='/notification/%s/star' % notification_id)

    def unstar(self, notification_id):
        return self.transport.DELETE(url='/notification/%s/star' % notification_id)


class Conversation(Area):
    def find_all(self):
        return self.transport.GET(url='/conversation/')

    def find(self, conversation_id):
        return self.transport.GET(url='/conversation/%s' % conversation_id)

    def create(self, attributes):
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/conversation/', body=attributes, type='application/json')

    def star(self, conversation_id):
        return self.transport.POST(url='/conversation/%s/star' % conversation_id)

    def unstar(self, conversation_id):
        return self.transport.DELETE(url='/conversation/%s/star' % conversation_id)

    def leave(self, conversation_id):
        return self.transport.POST(url='/conversation/%s/leave' % conversation_id)


class Files(Area):
    def find(self, file_id):
        pass

    def find_raw(self, file_id):
        """Returns raw file as string. Pass to a file object"""
        raw_handler = lambda resp, data: data
        return self.transport.GET(url='/file/%d/raw' % file_id, handler=raw_handler)

    def attach(self, file_id, ref_type, ref_id):
        attributes = {
            'ref_type': ref_type,
            'ref_id': ref_id
        }
        return self.transport.POST(url='/file/%s/attach' % file_id, body=json.dumps(attributes),
                                   type='application/json')

    def create(self, filename, filedata):
        """Create a file from raw data"""
        attributes = {'filename': filename,
                      'source': filedata}
        return self.transport.POST(url='/file/v2/', body=attributes, type='multipart/form-data')

    def copy(self, file_id):
        """Copy a file to generate a new file_id"""

        return self.transport.POST(url='/file/%s/copy' % file_id)


class View(Area):

    def create(self, app_id, attributes):
        """
        Creates a new view on the specified app

        :param app_id: the application id
        :param attributes: the body of the request as a dictionary
        """
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attributes = json.dumps(attributes)
        return self.transport.POST(url='/view/app/{}/'.format(app_id),
                                   body=attributes, type='application/json')

    def delete(self, view_id):
        """
        Delete the associated view

        :param view_id: id of the view to delete
        """
        return self.transport.DELETE(url='/view/{}'.format(view_id))

    def get(self, app_id, view_specifier):
        """
        Retrieve the definition of a given view, provided the app_id and the view_id

        :param app_id: the app id
        :param view_specifier:
            Can be one of the following:
            1. The view ID
            2. The view's name
            3. "last" to look up the last view used
        """
        return self.transport.GET(url='/view/app/{}/{}'.format(app_id, view_specifier))

    def get_views(self, app_id, include_standard_views=False):
        """
        Get all of the views for the specified app

        :param app_id: the app containing the views
        :param include_standard_views: defaults to false. Set to true if you wish to include standard views.
        """
        include_standard = "true" if include_standard_views is True else "false"
        return self.transport.GET(url='/view/app/{}/?include_standard_views={}'.format(app_id, include_standard))

    def make_default(self, view_id):
        """
        Makes the view with the given id the default view for the app. The view must be of type
        "saved" and must be active. In addition the user most have right to update the app.

        :param view_id: the unique id of the view you wish to make the default
        """
        return self.transport.POST(url='/view/{}/default'.format(view_id))

    def update_last_view(self, app_id, attributes):
        """
        Updates the last view for the active user

        :param app_id: the app id
        :param attributes: the body of the request in dictionary format
        """
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attribute_data = json.dumps(attributes)
        return self.transport.PUT(url='/view/app/{}/last'.format(app_id),
                                  body=attribute_data, type='application/json')

    def update_view(self, view_id, attributes):
        """
        Update an existing view using the details supplied via the attributes parameter

        :param view_id: the view's id
        :param attributes: a dictionary containing the modifications to be made to the view
        :return:
        """
        if not isinstance(attributes, dict):
            raise TypeError('Must be of type dict')
        attribute_data = json.dumps(attributes)
        return self.transport.PUT(url='/view/{}'.format(view_id),
                                  body=attribute_data, type='application/json')

