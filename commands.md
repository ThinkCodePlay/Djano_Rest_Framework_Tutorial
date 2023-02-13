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