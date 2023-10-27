from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Shopping

@api_view(['POST'])
def Create_Shopping(request):
	return Response(Shopping.create_shopping(request.data))

@api_view(['GET'])
def Verified_Invoice(request):
	return Response(Shopping.verified_invoice(request.data))	

