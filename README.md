PyPodio
=====

Python wrapper for the Podio API.

Install
-------

Dependencies

* httplib2

PyPodio is not yet available on PyPI, we're waiting to have it a bit more
stable. Install by cloning from the GitHub repo:

    $ git clone git://github.com/podio/podio-py.git
    $ cp -r podio-py/pypodio2 path/to/destination


Example
-------

    from pypodio2 import api
    from client_settings import *

    c = api.OAuthClient(
        client_id,
        client_secret,
        username,
        password,    
    )
    print c.Items.get_item(22342)

Notes
------

It is possible to override the default response handler by passing handler as
a keyword argument to a transport function call. For example:

    x = lambda x,y: (x,y)
    result = c.Items.find(11007, basic=True, handler=x)
    ($result, $data) #Returned info


Meta
----

* Code: `git clone git://github.com/podio/podio-py.git`
* Home: <https://github.com/podio/podio-py>
* Bugs: <https://github.com/podio/podio-py/issues>