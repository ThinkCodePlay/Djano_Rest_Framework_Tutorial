import requests

endpoint = "http://localhost:8001/api/"

# get_response = requests.get(endpoint, params={"abc": 123}, json={"query": "Hello World"}) # HTTP request
get_response = requests.post(endpoint, params={"abc": 123}, json={"title": "Hello World"}) # HTTP request

print('-----')
print(get_response.status_code)
print(get_response.json())
# print(get_response.json())