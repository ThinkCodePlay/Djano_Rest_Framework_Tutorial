
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.
@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        print(serializer.data)
        instance = serializer.save()
        data = serializer.data
        return Response(data)
    
