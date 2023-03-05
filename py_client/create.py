import requests

endpoint = "http://localhost:8001/api/products/"

data = {
    "title": "fiels is required",
    "price": 32.5,
}
get_response = requests.post(endpoint, json=data) # HTTP request

print('-----')
print(get_response.status_code)
print(get_response.json())