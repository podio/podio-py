from pypodio import *
import json
import settings

podio = Podio(client_id = settings.client_id, client_secret = settings.client_secret)
podio.request_oauth_token(settings.username, settings.password)

#Defined Method in 
print podio.users_get_active_profile()

#Undefined and created at runtime example
print podio.GET.user.status()

# Other methods are:
# podio.PUT.#{uri}.#{divided}.{by_slashes}()
# podio.DELETE.#{uri}.#{divided}.{by_slashes}()
# podio.POST.#{uri}.#{divided}.{by_slashes}(body=paramDict))
# For POST and PUT you can pass "type" as a kwarg and register the type as either
# application/x-www-form-urlencoded or application/json to match what API expects.