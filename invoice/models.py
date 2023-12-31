from django.db import models
from user.models import Employee
from company.models import Branch, License, Resolution
from inventory.models import Product
from customer.models import *
from django.core import serializers
from setting.models import *
import json

class Invoice(models.Model):
	type_document = models.IntegerField()
	number = models.IntegerField()
	prefix = models.CharField(max_length = 7) 
	branch = models.ForeignKey(Branch, on_delete = models.CASCADE)
	date = models.CharField(max_length = 12) 
	time = models.TimeField(auto_now_add = True)
	total = models.FloatField(null = True, blank = True)
	note = models.TextField(null = True, blank = True)
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
	cancelled = models.BooleanField(default = True)
	hidden = models.BooleanField(default = False)
	state = models.CharField(max_length = 70,null = True, blank = True)
	annulled = models.BooleanField(default = False)

	def __str__(self):
		return f"{self.prefix} - {self.number} by {self.branch.name}"

	@classmethod
	def get_invoice(cls, pk):
		_invoice = cls.objects.get(pk = pk)
		serialized_invoice = serializers.serialize('json', [_invoice])
		invoice = json.loads(serialized_invoice)[0]
		data = invoice['fields']
		data['pk_invoice'] = pk
		list_details = []
		for i in Details_Invoice.objects.filter(invoice = _invoice):
			serialized_invoice = serializers.serialize('json', [i])
			product = json.loads(serialized_invoice)[0]['fields']
			product['subtotals'] = (product['price'] + product['ipo']) * product['quantity']
			list_details.append(product)
		data['details'] = list_details
		serialized_paymentform = serializers.serialize('json', [Payment_Forms.objects.get(invoice = _invoice)])
		data['payment_form'] = json.loads(serialized_paymentform)[0]['fields']
		data['metod'] = "Crédito" if data['payment_form'] == 2 else "Efectivo"
		serialized_customer = serializers.serialize('json', [Customer.objects.get(pk = _invoice.customer.pk)])
		data['customer'] = json.loads(serialized_customer)[0]['fields']
		_branch = Branch.objects.get(pk = _invoice.branch.pk)
		branch = serializers.serialize('json', [_branch])
		data['branch'] = json.loads(branch)[0]['fields']
		resolution = serializers.serialize('json', [Resolution.objects.get(branch= _branch, type_document_id = data['type_document'])])
		data['resolution'] = json.loads(resolution)[0]['fields']

		return data



	@classmethod
	def annulled_invoice(cls, data):
		result = False
		message = None
		try:
			invoice = cls.objects.get(pk = data['pk_invoice'], annulled = False)
			invoice.total = 0
			invoice.annulled = True
			invoice.state = "Factura Anulada."
			invoice.save()
			for i in Details_Invoice.objects.filter(invoice = invoice):
				product = Product.objects.get(code = i.code)
				product.quantity += i.quantity
				product.save()
			result = True
			message = "Success"
			employee = Employee.objects.get(pk = data['pk_employee'])
			serialized_employee = serializers.serialize('json', [employee])
			employee = json.loads(serialized_employee)[0]['fields']
			serialized_invoice = serializers.serialize('json', [invoice])
			invoice = json.loads(serialized_invoice)[0]['fields']
			History_Invoice.create_history_invoice(invoice, employee, 'Annulled')
		except Exception as e:
			message = str(e)
			print(e)
		return {'result':result, 'message':message}

	@classmethod
	def get_list_invoice(cls, data):
		branch = Employee.objects.get(pk = data['pk_employee']).branch
		result = False
		message = None
		_data = None
		try:
			_data = [
				{
					"type_document":i.type_document,
					'pk_invoice': i.pk,
					'number': i.number,
					'prefix': i.prefix,
					'date': i.date,
					'name_client': i.customer.name,
					'total': i.total,
					"state":i.state
				}
				for i in cls.objects.filter(branch = branch, type_document = data['type_document'])
			]
		except Exception as e:
			print(e)
			message = str(e)
			_data = []
		return _data

	@classmethod
	def create_invoice(cls, data):
		result = False
		message = None
		employee = Employee.objects.get(pk = data['pk_employee'])
		total = 0
		pk_invoice = None
		customer = Customer.objects.get(pk = data['pk_client'])
		try:
			license = License.discount_license(employee.branch)
			if license['result']:
				invoice = cls(
					type_document = data['type_document'],
					number = data['number'],
					prefix = data['prefix'],
					branch = employee.branch,
					date = data['date'],
					note = data['note'],
					customer = customer,
					hidden = True if data['type_document'] == 99 else False,
					state = data['state']
				)
				invoice.save()
				pk_invoice = invoice.pk
				result = True
				message = "Success"
				if result:
					for i in data['details']:
						value = Details_Invoice.create_details(i, invoice)
						if not value['result']:
							result = False
							message = value['message']
							break
						else:
							result = value['result']
							message = value['message']
							total += float(value['total'])
				if result:
					value = Payment_Forms.create_paymentform(data, invoice)
					result = value['result']
					message = value['message']
					if result:
						pass
				invoice.total = total
				invoice.save()
				values_wallet = {"pk_customer":customer.pk, 'amount_invoice':total}
				Wallet_Customer.update_coins(data)
				data = {'type_document':data['type_document'], 'pk_branch':employee.branch.pk}
				Resolution.add_number(data)
				serialized_employee = serializers.serialize('json', [employee])
				employee = json.loads(serialized_employee)[0]['fields']
				serialized_invoice = serializers.serialize('json', [invoice])
				invoice = json.loads(serialized_invoice)[0]['fields']
				History_Invoice.create_history_invoice(invoice, employee, 'Created')
				
			else:
				result = license['result']
				message = license['message']
		except Exception as e:
			print(data)
			print(e,'error resolution')
			message = str(e)
		return {'result':result, 'message':message,'pk_invoice': pk_invoice}

	@classmethod
	def get_list_invoice_credit(cls, branch):
		return [
			{
				"pk_invoice" : i.pk,
				"number": i.number,
				"prefix": i.prefix,
				"date": i.date,
				"total": i.total,
				"pk_customer":i.customer.pk,	
				"name_customer":i.customer.name
			}
			for i in cls.objects.filter(branch = branch, cancelled = False).order_by('-date')
		]


class Details_Invoice(models.Model):
	code = models.CharField(max_length = 30)
	name = models.CharField(max_length = 150)
	quantity = models.IntegerField()
	tax = models.FloatField()
	cost = models.FloatField()
	price = models.FloatField()
	ipo = models.FloatField()
	discount = models.FloatField()
	invoice = models.ForeignKey(Invoice, on_delete = models.CASCADE)

	@classmethod
	def create_details(cls, data, invoice):
		result = False
		message = None
		try:
			details_invoice = cls(
				code = data['code'],
				name = data['product'],
				quantity = data['quantity'],
				tax = data['tax'],
				cost = 0,
				price = data['price'],
				ipo = data['ipo'],
				discount = data['discount'],
				invoice = invoice
			)
			details_invoice.save()
			result = True
			message = "Success"
			if result:
				if invoice.type_document != 99:
					value = Product.discount_product(data['code'], invoice.branch, int(data['quantity']))
					if not value['result']:
						result = value['result']
						message = value['message']
						invoice.delete()
						return {'result':result, 'message':message}
		except Exception as e:
			message = str(e)
			print(e)

		return {'result':result, 'message':message,'total':data['price']}


class Payment_Forms(models.Model):
	payment_form = models.ForeignKey(Payment_Form, on_delete = models.CASCADE)
	payment_method = models.ForeignKey(Payment_Method, on_delete = models.CASCADE)
	payment_due_date = models.CharField(max_length = 12)
	invoice = models.ForeignKey(Invoice, on_delete = models.CASCADE)

	@classmethod
	def create_paymentform(cls, data, invoice):
		result = False
		message = None
		try:
			payment_form = cls(
				payment_form = Payment_Form.objects.get(_id = data['payment_form']['paymentform']),
				payment_method = Payment_Method.objects.get(_id = data['payment_form']['paymentmethod']),
				payment_due_date = data['payment_form']['due_date'],
				invoice = invoice
			)
			payment_form.save()
			if data['payment_form']['paymentform'] == 2:
				invoice.cancelled = False
				invoice.save()
				_data = {
					"pk_invoice": invoice.pk,
					"amount":0,
					"note":"There are no pass yet",
					"employee": data['pk_employee']
				}
				Pass.create_pass(_data)
				result = True
				message = "Success"
			else:
				employee = Employee.objects.get(pk = data['pk_employee'])
				serialized_product = serializers.serialize('json', [employee])
				employee = json.loads(serialized_product)[0]['fields']
				value = History_Invoice.create_history_invoice(data, employee, 'Created')
				result = value['result']
				message = value['message']
		except Exception as e:
			print(e)
			message = f"{e} - Error Payment Form"
		return {'result':result, 'message':message}

class Pass(models.Model):
	number_pass = models.IntegerField()
	invoice = models.ForeignKey(Invoice, on_delete = models.CASCADE)
	amount = models.FloatField()
	date = models.DateTimeField(auto_now_add = True)
	note = models.TextField()
	employee = models.JSONField(null = True, blank = True)

	@classmethod
	def create_pass(cls, data):
		try:
			number = len(cls.objects.all())
		except Exception as e:
			print(e)
		invoice = Invoice.objects.get(pk = data['pk_invoice'])
		result = False
		message = None
		try:
			_pass = cls.objects.get(invoice = invoice)
			if _pass.amount < invoice.total:
				if float(data['amount']) <= (invoice.total - _pass.amount) and float(data['amount']) > 0:
					_pass.amount += float(data['amount'])
					message = "Credit to the invoice was accepted"
					result = True
				else:
					message = "You cannot pay more than the total invoice"
		except cls.DoesNotExist as e:
			_pass = cls(
				number_pass = number if number > 0 else 1,
				invoice = invoice,
				amount = data['amount'],
				note = data['note']
			)
			message = f"Credit to the invoice {invoice.number} was created successfully"
			result = True
		_pass.save()
		if _pass.amount == invoice.total:
			invoice.cancelled = True
			invoice.save()
			message = "The invoice has already been canceled"

		serialized_invoice = serializers.serialize('json', [invoice])
		serialized_customer = serializers.serialize('json', [invoice.customer])

		customer = json.loads(serialized_customer)[0]['fields']
		invoice = json.loads(serialized_invoice)[0]['fields']

		employee = Employee.objects.get(pk = data['pk_employee'])
		employee = serializers.serialize('json', [employee])

		if result:
			History_Pass.create_history_pass(invoice, data['amount'], customer, data['note'], employee)
		return {'result':True, 'message':message}

	@classmethod
	def cancel_all_invoices(cls, data):
		employee = Employee.objects.get(pk = data['pk_employee'])
		customer = Customer.objects.get(pk = data['pk_customer'])
		pk = customer.pk
		invoice = Invoice.objects.filter(branch= employee.branch, cancelled = False, customer = customer)
		total = 0
		result = False
		message = None
		amount = data['amount']
		for i in invoice:
			total += i.total

		if total == amount:
			for i in invoice:
				_pass = cls.objects.get(invoice = i)
				_pass.amount = i.total
				_pass.save()
				i.cancelled = True
				i.save()
				result = True
				message = "Invoice paid"
		else:
			note = None
			for i in invoice:
				if amount >= i.total:
					_pass = cls.objects.get(invoice = i)
					_pass.amount = i.total
					amount -= i.total
					i.cancelled = True
					_pass.save()
					note = "Pago factura"
					serialized_invoice = serializers.serialize('json', [i])
					serialized_customer = serializers.serialize('json', [i.customer])
					customer = json.loads(serialized_customer)[0]['fields']
					_invoice = json.loads(serialized_invoice)[0]['fields']
					_employee = serializers.serialize('json', [employee])
					__employee = json.loads(_employee)[0]['fields']
					History_Pass.create_history_pass(_invoice, data['amount'], customer, note , __employee)
				else:
					_pass = cls.objects.get(invoice = i)
					_pass.amount += amount
					_pass.save()
					note = "Abona a la factura"
					serialized_invoice = serializers.serialize('json', [i])
					serialized_customer = serializers.serialize('json', [i.customer])
					customer = json.loads(serialized_customer)[0]['fields']
					_invoice = json.loads(serialized_invoice)[0]['fields']
					_employee = serializers.serialize('json', [employee])
					__employee = json.loads(_employee)[0]['fields']
					History_Pass.create_history_pass(_invoice, data['amount'], customer, note , __employee)
					if not _pass.invoice.cancelled:
						amount -= _pass.amount
						if amount <= 0:
							break
				i.save()
				result = True
				message = "Invoice paid"
		values = {"pk_customer": pk, "amount": amount}
		Wallet_Customer.update_wallet_customer(data)
		return {'result':result, 'message':message,"returned_value":amount}



class History_Invoice(models.Model):
	ACTION_CHOICES = (
	    ('Created', 'Created'),
	    ('Modified', 'Modified'),
	    ('Deleted', 'Deleted'),
	    ('Annulled', 'Annulled'),
	)
	action = models.CharField(max_length=10, choices=ACTION_CHOICES,null = True, blank = True)
	invoice = models.JSONField()
	employee = models.JSONField()
	date_registration = models.DateTimeField(auto_now_add = True)

	@classmethod
	def create_history_invoice(cls, invoice, employee, action):
		result = False
		message = None
		try:
			hi = cls(
				invoice = invoice,
				employee = employee,
				action = action
			)
			hi.save()
			result = True
			message = "Success"
		except Exception as e:
			message = str(e)
			print(e,'Error History_Invoice')
		return {'result':result, 'message':message}


class History_Pass(models.Model):
	invoice = models.JSONField(null = True, blank = True)
	amount = models.FloatField(null = True, blank = True)
	customer = models.JSONField(null = True, blank = True)
	employee = models.JSONField(null = True, blank = True)
	note = models.TextField(null = True, blank = True)
	date_registration = models.DateTimeField(auto_now_add = True)

	@classmethod
	def create_history_pass(cls, invoice, amount, customer, note, employee):
		result = False
		message = None
		try:
			hp = cls(
				invoice = invoice,
				amount = amount,
				customer = customer,
				note = note,
				employee = employee
			)
			hp.save()
			result = True
			message = "Success"
		except Exception as e:
			print(e)
			message = str(e)
		return {'result':result, 'message':message}