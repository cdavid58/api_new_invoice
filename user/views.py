from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee

@api_view(['POST'])
def Create_Employee(request):
	return Response(Employee.create_employee(request.data))

@api_view(['POST'])
def Login(request):
	return Response(Employee.login(request.data))

@api_view(['GET'])
def Get_List_Employee(request):
	return Response(Employee.get_list_employee(request.data))

@api_view(['GET'])
def Get_Employee(request):
	return Response(Employee.get_employee(request.data))


@api_view(['PUT'])
def LogOut(request):
	return Response(Employee.logout(request.data))

@api_view(['PUT'])
def Update_User(request):
	return Response(Employee.Update_User(request.data))