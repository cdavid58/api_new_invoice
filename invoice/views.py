from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *

@api_view(['POST'])
def Create_Invoice(request):
	return Response(Invoice.create_invoice(request.data))


@api_view(['POST'])
def Create_Pass_Invoice(request):
	return Response(Pass.create_pass(request.data))

@api_view(['POST'])
def Cancel_All_Invoice(request):
	return Response(Pass.cancel_all_invoices(request.data))

@api_view(['GET'])
def Get_List_Invoice(request):
	return Response(Invoice.get_list_invoice(request.data))	

@api_view(['POST'])
def Annulled_Invoice(request):
	return Response(Invoice.annulled_invoice(request.data))	

