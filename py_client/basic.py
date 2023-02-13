import requests

endpoint = "http://localhost:8001/api"

get_response = requests.get(endpoint) # HTTP request

print(get_response.text)
print(get_response.status_code)
# print(get_response.json())