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

## DetailAPIView
in products.views make an single fetch endpoint:

```python
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

# when using Detail this means we want to get only one item
class ProductDetailAPIView(generics.RetrieveAPIView): 
    queryset = Product.objects.all() # used to query the data
    serializer_class = ProductSerializer 
    # lookup_field = 'pk' # equivelent to Product.objects.get(pk='abc'). when fetching one item use the lookup_field
```

add the urls in urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.ProductDetailAPIView.as_view())
]
```
since we are using generic API view we can use the pk as the the lookup field as the url parameter.

then add the view url to the the apps urls
```python
# cfehome.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/products/', include('products.urls'))
]
```

## CreateAPIView
let's make another api view to create new products

```python
#views.py
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```
```python
# urls.py
urlpatterns = [
    path("", views.ProductCreateAPIView.as_view()),
    path('<int:pk>/', views.ProductDetailAPIView.as_view())
]
```
```python
#create.py py_client
import requests

endpoint = "http://localhost:8001/api/products/"

data = {
    "title": "fiels is required"
}
get_response = requests.post(endpoint, json=data) # HTTP request

print('-----')
print(get_response.status_code)
print(get_response.json())
```

when using generics you can use their built in functions such as on what to do on create. when using CreateAPIView you have the perform_create function

```python
class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        content = serializer.validated_data.get('content', 'no content')
        serializer.save(content=content)
```
## ListAPIView
The straigh forward way is to do the same as we did untill now
```python
class ProductListAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```
and then add to the ursl. but there is another option we can use.
we can instead use a ListCreateAPIView and replace the CreateAPIView, and rename the url:

```python
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        content = serializer.validated_data.get('content', 'no content')
        serializer.save(content=content)
```
```python
urlpatterns = [
    path("", views.ProductListCreateAPIView.as_view()),
    path('<int:pk>/', views.ProductDetailAPIView.as_view())
]
```

Now ProductListCreateAPIView is userd with POST to create and GET to fetch list of items.

going to http://localhost:8001/api/products/ will also show us both the list and the option to create.


# Function Based Views

An alternative to using class based views is function baes views. 
This is done by using the @api_view decorator and checking what the method is.
Here's how we would replace the above code with function based views:
```python
# from function based views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            # detail view
            qs = Product.objects.filter(pk=pk)
            if not qs.exists():
                raise Http404 # this is recognized by the @api_view decorator.
            return Response()
        else: 
            # list view
            qs = Product.objects.all() # queryset
            data = ProductSerializer(qs, many=True).data
            return Response(data)
    
    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            content = serializer.validated_data.get('content', 'no content')
            serializer.save(content=content)
            return Response(serializer.data)
```
we can also use rest framework shorcut for fetching a single instance:
```python
...
    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        else: 
...
```

## Update and Destroy API

Update and delete class based views:
```python
class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()

class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # here you can do stuff with the instance
        print(instance)
        return super().perform_destroy(instance)
```
```python
urlpatterns = [
    path("", views.ProductListCreateAPIView.as_view()),
    path('<int:pk>/update/', views.ProductUpdateAPIView.as_view()),
    path('<int:pk>/delete/', views.ProductDeleteAPIView.as_view()),
    path('<int:pk>/', views.ProductDetailAPIView.as_view()),
]
```



---
#Stoped tutorial at [this point](https://youtu.be/c708Nf0cHrs?t=7444).


