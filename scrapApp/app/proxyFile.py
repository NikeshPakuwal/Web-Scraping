# importing the requests library
import requests

# Proxies api-endpoint
URL = "http://api.proxiesapi.com"

# insert your auth key here
auth_key = "8aaf4535c3d7b6e0efd39ffe898f6efa_sr98766_ooPq87"
url = "http://httpbin.org/anything"
session = "444"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'auth_key': auth_key, 'url': url, 'render': 'true'}

# sending get request and saving the response as response object
r = requests.get(url=URL, params=PARAMS)

print(r.text)

# sending get request and saving the response as response object
# r = requests.get(url=URL, params=PARAMS)
