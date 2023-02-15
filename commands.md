# Tutorial

## Setup
```bash
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
django-admin startproject cfehome .
```
## Run Server
```bash
python3 manage.py runserver 8001
```

## Start new app:
```bash
python3 manage.py startapp api
```

Add the app to settings.py

```python
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api'
]
...
```

in the app folder in views.py add the endpoint:
```python
from django.http import JsonResponse

# Create your views here.
def api_home(request, *args, **kwargs):
    return JsonResponse({"message": "Hi This is you Django API Response"})
```

add a urls.py folder
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_home)
]
```

now import it to the global urls
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]
```
now run the server again
```bash
python3 manage.py runserver 8001
```

## Api with models:
```bash
python3 manage.py startapp products                                    
```

in models.py add a new model:
```python
from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
```
then run migration
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## To run shell:
```bash
python manage.py shell
```
```python
from products.models import Product
Product.objects.create(title="Book", content="Harry Potter", price="12.00")
Product.objects.create(title="Book", content="The Dome", price="39.00")
Products.objects.all()
```

## To Switch to DRF:
```python
from rest_framework.response import response
from rest_framework.decorators import api_view

@api_view(["GET"])
def api_home(request, *args, **kwargs):
...
```

## create serializer in products
```python
from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        field = [
            'title', 'content', 'price', 'sale_price'
        ]
        fields = '__all__'
```
then import it into your view:
```python

from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.
@api_view(["GET"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    instance = Product.objects.all().order_by("?").first()
    data = {}
    if instance:
        data = ProductSerializer(instance).data

    return Response(data)
```

currently http://localhost:8001/api/ does not exist.
to make it work add to settings.py:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    ...
]
```

lets make a POST method and check that the data revieved is valid:

```python
get_response = requests.post(endpoint, params={"abc": 123}, json={"title": "Hello World"}) # HTTP request
```
```python
@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.data)
        data = serializer.data
        return Response(data)
```
If we want to use the data we can save the data
```python
instance = serializer.save()
```

you can make validation throw error using rais_exception:
```python
if serializer.is_valid(raise_exception=True):
```

# Generic API views




---
<!-- #Stoped at [injest data with DRF views](https://youtu.be/c708Nf0cHrs?t=4486) -->


