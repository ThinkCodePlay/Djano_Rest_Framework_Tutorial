import requests

endpoint = "http://localhost:8001/api/products/1/"

get_response = requests.get(endpoint) # HTTP request

print('-----')
print(get_response.status_code)
print(get_response.json())