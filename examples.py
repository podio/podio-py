from pypodio import *
import json
import settings

podio = Podio(client_id = settings.client_id, client_secret = settings.client_secret)
print podio.request_oauth_token(settings.username, settings.password)

#Defined Method in 
#print podio.users_get_active_profile()
#print podio._headers

print podio.space_find_by_url("https://remaxtraditions.podio.com/remaxtraditions/")

print podio.space_create(dict(org_id=6883, name= "test", post_on_new_app = False, post_on_new_member = False))
#print podio.app_list_apps_in_space("remaxtraditions")

#Undefined and created at runtime example
#print podio.GET.user.status()

# Other methods are:
# podio.PUT.#{uri}.#{divided}.{by_slashes}()
# podio.DELETE.#{uri}.#{divided}.{by_slashes}()
# podio.POST.#{uri}.#{divided}.{by_slashes}(body=paramDict))
# For POST and PUT you can pass "type" as a kwarg and register the type as either
# application/x-www-form-urlencoded or application/json to match what API expects.