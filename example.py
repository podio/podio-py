client_id = ""
client_secret = ""
username = ""
password = ""

from pypodio2 import api

c = api.OAuthClient(
    client_id,
    client_secret,
    username,
    password,    
)


print c.Item.find(22481) #Get https://hoist.podio.com/api/item/22481
print c.Space.find_by_url("https://remaxtraditions.podio.com/remaxtraditions/") #Find ID

items = c.Application.get_items(48294)['items']


#To create an item
item = {
	"fields":[
		{"external_id":"org-name", "values":[{"value":"The Items API sucks"}]}
	]
}
#print c.Application.find(179652)
c.Item.create(app_id, item)
			
#Undefined and created at runtime example
#print c.transport.GET.user.status()

# Other methods are:
# c.transport.PUT.#{uri}.#{divided}.{by_slashes}()
# c.transport.DELETE.#{uri}.#{divided}.{by_slashes}()
# c.transport.POST.#{uri}.#{divided}.{by_slashes}(body=paramDict))
# For POST and PUT you can pass "type" as a kwarg and register the type as either
# application/x-www-form-urlencoded or application/json to match what API expects.

#items[0]['fields'][2]['values'][0]['value']['file_id']
