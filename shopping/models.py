from django.db import IntegrityError
from inventory.models import Product, Supplier
from setting.models import Payment_Form, Payment_Method
from django.core import serializers
from company.models import Branch, License
from user.models import Employee
from django.db import models
import json

class Shopping(models.Model):
	number = models.CharField(max_length = 50, unique = True)
	date = models.DateTimeField(auto_now_add = True)
	branch = models.ForeignKey(Branch, on_delete = models.CASCADE)
	supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE) 
	date_registration = models.CharField(max_length = 10)

	def __str__(self):
		return f"{self.number} by {self.branch.name} - {self.date}"

	@classmethod
	def verified_invoice(cls, data):
		result = False
		message = None
		try:
			cls.objects.get(number=data['number'], branch = Employee.objects.get(pk = data['pk_employee']).branch)
			result = True
			message = "Esta factura de compra ya existe."
		except cls.DoesNotExist as e:
			message = None
		return {'result':result, 'message':message}

	@classmethod
	def create_shopping(cls, data):
		result = False
		message = None
		try:
			branch = Employee.objects.get(pk = data['pk_employee']).branch
			value = License.discount_license(branch)
			if value['result']:
				shopping = cls(
					number = data['number'],
					branch = branch,
					supplier = Supplier.objects.get(pk = data['pk_supplier']),
					date_registration = data['date_registration'],
				)
				shopping.save()
				result = True
				message = "Success"
				for i in data['details']:
					result = Details.create_details(i, shopping)
					if not result['result']:
						message = result['message']
						result = result['result']
						break
				result = PaymentFormShopping.create_payment_form(data, shopping)
				if not result['result']:
					message = result['message']
					result = result['result']
				else:
					result = result['result']
			else:
				result = value['result']
				message = value['message']
		except IntegrityError as inte:
			message = "This invoice has already been registered."
		except Exception as e:
			message = f"{e} - Shopping Invoice"
		return {'result':result, 'message':message}


class Details(models.Model):
	code = models.CharField(max_length = 30)
	name = models.CharField(max_length = 150)
	quantity = models.IntegerField()
	tax = models.IntegerField()
	cost = models.FloatField()
	price_1 = models.FloatField()
	price_2 = models.FloatField()
	price_3 = models.FloatField()
	ipo = models.FloatField()
	discount = models.FloatField()
	shopping = models.ForeignKey(Shopping, on_delete = models.CASCADE)

	def __str__(self):
		return f"{self.shopping.number} by {self.shopping.branch.name} - {self.shopping.date}"

	@classmethod
	def create_details(cls,data,shopping):
		result = False
		message = None
		try:
			details = cls(
				code= data['code'],
			    name= data['name'],
			    quantity= data['quantity'],
			    tax= data['tax'],
			    cost= data['cost'],
			    price_1= data['price_1'],
			    price_2= data['price_2'],
			    price_3= data['price_3'],
			    ipo= data['ipo'],
			    discount= data['discount'],
			    shopping= shopping
			)
			details.save()
			result = True
			message= "Success"
			if result:
				result = cls.update_product_by_shopping(data, shopping)
			message = result['message']
			result = result['result']
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}


	@staticmethod
	def update_product_by_shopping(data, shopping):
		result = False
		message = None
		try:
			product = Product.objects.get(code = data['code'], branch=shopping.branch)
			product.tax = data['tax']
			product.quantity += int(data['quantity'])
			product.price_1 = data['price_1']
			product.price_2 = data['price_2']
			product.price_3 = data['price_3']
			product.ipo = data['ipo']
			product.discount = data['discount']
			product.save()
			result = True
			message = "Success"
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}


class PaymentFormShopping(models.Model):
	shopping = models.ForeignKey(Shopping, on_delete = models.CASCADE)
	payment_form = models.ForeignKey(Payment_Form, on_delete = models.CASCADE)
	payment_method = models.ForeignKey(Payment_Method, on_delete = models.CASCADE)
	payment_due_date = models.CharField(max_length = 10)

	def __str__(self):
		return f"{self.shopping.number} by {self.shopping.branch.name} - {self.shopping.date}"

	@classmethod
	def create_payment_form(cls, data, shopping):
		result = False
		message = None
		try:
			payment_form = cls(
				shopping = shopping,
				payment_form = Payment_Form.objects.get(_id = data['payment_form']['pk_paymentform']),
				payment_method = Payment_Method.objects.get(_id = data['payment_form']['pk_paymentmethod']),
				payment_due_date = data['payment_form']['payment_due_date']
			)
			payment_form.save()
			result = True
			message = "Success"
			employee = Employee.objects.get(pk = data['pk_employee'])
			serialized_product = serializers.serialize('json', [employee])
			employee = json.loads(serialized_product)[0]['fields']
			value = History_Shopping.create_history(data,employee)
			result = value['result']
			message = value['message']
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}

class History_Shopping(models.Model):
	invoice = models.JSONField()
	employee = models.JSONField()
	date_registration = models.DateTimeField(auto_now_add = True)

	@classmethod
	def create_history(cls,invoice, employee):
		result = False
		message = None
		try:
			hs = cls(
				invoice = invoice,
				employee = employee
			)
			hs.save()
			result = True
			message = "Success"
		except Exception as e:
			message = str(e)
		return {'result': result, 'message':message}

