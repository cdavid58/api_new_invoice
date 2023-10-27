from rest_framework.decorators import api_view
from rest_framework.response import Response
from invoice.models import Invoice
from user.models import Employee

@api_view(['GET'])
def Get_List_Invoice_Credit(request):
	branch = Employee.objects.get(pk = request.data['pk_employee']).branch
	return Response(Invoice.get_list_invoice_credit(branch))
