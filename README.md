PyPodio
=====

Python wrapper for the Podio API.

Install
-------

PyPodio is not yet available on PyPI, we're waiting to have it a bit
more stable. Install by cloning from the GitHub repo:

    $ git clone git://github.com/podio/podio-py.git
    $ 


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

Meta
----

* Code: `git clone git://github.com/podio/podio-py.git`
* Home: <https://github.com/podio/podio-py>
* Bugs: <https://github.com/podio/podio-py/issues>