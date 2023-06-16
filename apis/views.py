from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
# import viewsets
from rest_framework import viewsets
from django.core.serializers import serialize
from django.forms.models import model_to_dict


# import local data
from .serializers import GeeksSerializer
from .models import GeeksModel

# create a viewset
class GeeksViewSet(viewsets.ModelViewSet):
	# define queryset
	queryset = GeeksModel.objects.all()
	
	# specify serializer to be used
	serializer_class = GeeksSerializer

def products(request, prod_id):
    try:
        prod = GeeksModel.objects.get(id=prod_id)
        prod_dict = {
            "id": prod.id,
            "price": prod.price,
            "description": prod.description,
            "photo": prod.photo.url if prod.photo else None,
        }
        response = JsonResponse(prod_dict)
        response['Content-Type'] = 'application/json'
        return response
    except GeeksModel.DoesNotExist:
        response = JsonResponse({"error": "Product not found"})
        response.status_code = 404
        return response