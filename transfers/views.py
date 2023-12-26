from rest_framework.response import Response
from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view

@api_view(['POST'])
def Save_Transfer(request):
	return Response(Transfer.transfer_products(request.data))