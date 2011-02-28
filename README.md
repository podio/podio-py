PyPodio
=====

Python wrapper for the Podio API.

Install
-------

PyPodio is not yet available on PyPI, we're waiting to have it a bit
more stable. Install by cloning from the GitHub repo:

    $ git clone git://github.com/podio/podio-py.git
    $ cd podio-py
    $ python setup.py build
    $ python setup.by install


Example
-------

    import pypodio
    
    podio = pypodio.Podio(
    	client_id = $your_client_id,
    	client_secret = $your_client_secret
    )
	podio.request_oauth_token($your_username, $your_password)


    # Get your user profile
    profile = podio.users_get_active_profile()

    print profile  

Meta
----

* Code: `git clone git://github.com/podio/podio-py.git`
* Home: <https://github.com/podio/podio-py>
* Bugs: <https://github.com/podio/podio-py/issues>