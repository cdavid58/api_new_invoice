from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import *

@api_view(['POST'])
def Create_Product(request):
	return Response(Product.create_product(request.data))

@api_view(['PUT'])
def Update_Product(request):
	return Response(Product.update_product(request.data))

@api_view(['DELETE'])
def Delete_Product(request):
	return Response(Product.delete_product(request.data))

@api_view(['POST'])
def Create_Supplier(request):
	return Response(Supplier.create_supplier(request.data))

@api_view(['PUT'])
def Update_Supplier(request):
	return Response(Supplier.update_supplier(request.data))

@api_view(['GET'])
def Get_List_Products(request):
	return Response(Product.get_list_products(request.data))

@api_view(['GET'])
def Get_Product(request):
	return Response(Product.get_product(request.data))	

@api_view(['GET'])
def List_Supplier(request):
	return Response(Supplier.list_supplier(request.data))

@api_view(['POST'])
def Delete_Supplier(request):
	return Response(Supplier.delete_supplier(request.data))

@api_view(['GET'])
def Get_Supplier(request):
	return Response(Supplier.get_supplier(request.data))

@api_view(['GET'])
def Get_Category(request):
	return Response(Category.get_list_category())

@api_view(['POST'])
def Get_SubCategory(request):
	return Response(SubCategory.get_list_subcategory(request.data))

@api_view(['GET'])
def Get_List_Products_Supplier(request):
	return Response(Product.get_list_products_supplier(request.data))


