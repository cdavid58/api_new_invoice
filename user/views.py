from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee

@api_view(['POST'])
def Create_Employee(request):
	return Response(Employee.create_employee(request.data))

@api_view(['POST'])
def Login(request):
	return Response(Employee.login(request.data))