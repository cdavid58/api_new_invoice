from django.db import models
from shopping.models import Shopping, PaymentFormShopping, Pass as p
from invoice.models import Invoice, Payment_Forms, Pass
from datetime import datetime


class Wallet(models.Model):

	@classmethod
	def get_pass_invoice(cls,data):
		invoice = Invoice.objects.filter(branch = data['pk_branch'], cancelled = False)
		data = []
		for i in invoice:
			print(i)
			_pass = Pass.objects.get(invoice = i)
			payment_forms = Payment_Forms.objects.get(invoice = i)
			date_start = datetime.strptime(i.date, "%Y-%m-%d")
			date_end = datetime.strptime(payment_forms.payment_due_date, "%Y-%m-%d")
			difference_in_days = (date_end - date_start).days
			data.append({
				'pk_invoice':i.pk,
				"number":i.number,
				"identification_number":f"{i.customer.identification_number}-{i.customer.dv}",
				"name_client": i.customer.name,
				"date": date_start.strftime("%Y-%m-%d"),
				"due_date": date_end.strftime("%Y-%m-%d"),
				"total": i.total,
				"pass": _pass.amount,
				"total_to_pay": i.total - _pass.amount,
				"difference_in_days" : difference_in_days,
				"arrears": True if difference_in_days < 0 else False
			})
		return data


	@classmethod
	def get_pass_shopping(cls, data):
	    shopping = Shopping.objects.filter(branch=data['pk_branch'], cancelled=False)
	    result_data = []
	    for i in shopping:
	    	if len(shopping) > 0:
		        _pass = p.objects.get(shopping=i)
		        payment_forms = PaymentFormShopping.objects.get(shopping=i)
		        date_start = i.date
		        date_end = datetime.strptime(payment_forms.payment_due_date, "%Y-%m-%d")
		        difference_in_days = (date_end - date_start).days
		        result_data.append({
		            'pk_invoice': i.pk,
		            "number": i.number,
		            "identification_number": f"{i.supplier.documentI}",
		            "name_client": i.supplier.name,
		            "date": date_start.strftime("%d-%m-%Y"),
		            "due_date": date_end.strftime("%d-%m-%Y"),
		            "total": i.total,
		            "pass": _pass.amount,
		            "total_to_pay": i.total - _pass.amount,
		            "difference_in_days": difference_in_days,
		            "arrears": True if difference_in_days < 0 else False
		        })
	    return result_data