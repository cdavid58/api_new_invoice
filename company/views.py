from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.shortcuts import render
from .models import *


@api_view(['POST'])
def Create_Company(request):
	ip_address = request.META.get('REMOTE_ADDR', '')
	print(ip_address)
	return JsonResponse(Company.create_company(request.data))
 
@api_view(['POST'])
def Create_Branch(request):
	return JsonResponse(Company.create_branch(request.data))
 
@api_view(['PUT'])
def Update_Resolution(request):
	return JsonResponse(Resolution.update_resolution(request.data))

@api_view(['POST'])
def Create_Resolution(request):
	return JsonResponse(Resolution.create_resolution(request.data,Branch.objects.get(pk = request.data['pk_branch'])))	

@api_view(['GET'])
def Get_Resolution(request):
	return JsonResponse(Resolution.get_resolution(request.data))	