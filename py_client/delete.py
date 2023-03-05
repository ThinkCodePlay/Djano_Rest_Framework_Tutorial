import requests

endpoint = "http://localhost:8001/api/products/9/delete/"

get_response = requests.delete(endpoint) # HTTP request

print('-----')
print(get_response.status_code)