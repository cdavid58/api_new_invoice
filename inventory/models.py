from django.db import IntegrityError
from company.models import Branch
from django.db import models
from user.models import Employee
from django.core import serializers
from django.http import JsonResponse
import json


class Supplier(models.Model):
	documentI = models.IntegerField(null = True, blank = True)
	name = models.CharField(max_length = 70)
	email = models.EmailField(null = True, blank = True)
	phone = models.CharField(max_length = 15,null = True, blank = True)
	branch = models.ForeignKey(Branch, on_delete = models.CASCADE)

	def __str__(self):
		return f"{self.name} by {self.branch.name}"

	@classmethod
	def create_supplier(cls,data):
		result = True
		message = None
		try:
			supplier = cls(
				documentI = data['documentI'],
				name = data['name'],
				email = data['email'],
				phone = data['phone'],
				branch = Employee.objects.get(pk = data['pk_employee']).branch
			)
			supplier.save()
			message = "Successs"
		except Exception as e:
			message = str(e)
		return {'result': result, 'message':message}

	@classmethod
	def update_supplier(cls,data):
		result = True
		message = None
		try:
			supplier = cls.objects.get(pk = data['pk_supplier'])
			supplier.documentI = data['documentI']
			supplier.name = data['name']
			supplier.email = data['email']
			supplier.phone = data['phone']
			supplier.save()
			message = "Successs"
		except Exception as e:
			message = str(e)
		return {'result': result, 'message':message}

	@classmethod
	def list_supplier(cls, data):
		branch = Employee.objects.get(pk = data['pk_employee']).branch
		return [
			{
				"pk": i.pk,
				"documentI": i.documentI if i.documentI else "No tiene",
				"name": i.name,
				"email": i.email if i.email else "No tiene",
				"phone": i.phone if i.phone else "No tiene"
			}
			for i in cls.objects.filter(branch = branch)
		]

	@classmethod
	def get_supplier(cls,data):
		return json.loads( serializers.serialize('json', [cls.objects.get(pk = data['pk_supplier'])]))[0]['fields']

	@classmethod
	def delete_supplier(cls,data):
		branch = Employee.objects.get(pk = data['pk_employee']).branch
		result = True
		message = None
		try:
			cls.objects.get(branch = branch, pk = data['pk_suppplier']).delete()
			result = True
			message = "Success"
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}

class Category(models.Model):
	name = models.CharField(max_length = 150, unique= True)

	def __str__(self):
		return self.name

	@classmethod
	def create_category(cls,data):
		category = cls(name = data['category'])
		category.save()
		for i in data['data']:
			if not create_subcategory(cls,i['name'],category.pk)['result']:
				break

	@classmethod
	def get_list_category(cls):
		return [
			{
				'pk_category':i.pk,
				'name': i.name
			}
			for i in cls.objects.all()
		]

class SubCategory(models.Model):
	name = models.CharField(max_length = 150, unique = True)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	def __str__(self):
		return self.name

	@classmethod
	def create_subcategory(cls,name,pk):
		message = None
		result = False
		try:
			cls(name = name,category=pk).save()
			message = 'Success'
			result = True
		except IntegrityError as e:
			message = str(e)
		return {'message':message, 'result':result}


	@classmethod
	def get_list_subcategory(cls, data):
		list_sub = []
		category = Category.objects.get(pk = data['pk_category'])
		for i in cls.objects.filter(category = category):
			serialized_subcategory = serializers.serialize('json', [i])
			subc = json.loads(serialized_subcategory)
			data = subc[0]['fields']
			data['pk_sub'] = subc[0]['pk']
			list_sub.append(data)
		return list_sub

class Product(models.Model):
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
	branch = models.ForeignKey(Branch, on_delete = models.CASCADE)
	subcategory = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
	supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, null = True, blank = True)

	def __str__(self):
		return self.name

	def calculate_profit_percentages(self):
		profit_percentages = {}
		prices = {
			'price': self.price,
			'price2': self.price2,
			'price3': self.price3,
			'price4': self.price4,
			'price5': self.price5
		}
		for price_field, price in prices.items():
			profit = (price - self.cost) * self.quantity
			profit_percentage = (profit / (self.cost * self.quantity)) * 100
			profit_percentages[price_field] = profit_percentage
		return profit_percentages

	@staticmethod
	def calculate_profit_amount(self):
	    profit_amounts = {}
	    prices = {
			'Precio 1': self.price_1,
			'Precio 2': self.price_2,
			'Precio 3': self.price_3,
		}

	    for price_field, price in prices.items():
	        try:
	            profit_percentage = ((price - self.cost) / price) * 100
	            profit_amount = (profit_percentage / 100) * price  # Calculate the amount of profit in money
	            profit_amounts[price_field] = profit_amount
	        except ZeroDivisionError as e:
	            profit_amounts[price_field] = 0
	    return profit_amounts

	def calculate_profit_percentages_one_quantity(self):
		profit_percentages = []
		prices = {
		    'Precio 1': self.price_1,
		    'Precio 2': self.price_2,
		    'Precio 3': self.price_3,
		}
		n = 1
		for price_field, price in prices.items():
		    try:
		        discounted_price = price - (price * (self.discount / 100))
		        if discounted_price == self.cost:
		            profit_percentage = 0  # If price equals cost after discount, profit percentage is 0
		        else:
		            profit_percentage = (((discounted_price - self.cost) / discounted_price) * 100)
		        profit_percentages.append({
		            'percentage': f'{profit_percentage:.1f}%',
		            'name': price_field,
		            'id': n
		        })
		    except ZeroDivisionError as e:
		        profit_percentages.append({
		            'percentage': '0%',
		            'name': price_field,
		            'id': n
		        })
		    n += 1

		return profit_percentages



	@staticmethod
	def Delete_Product_All(cls, branch):
		for i in cls.objects.filter(branch = branch):
			i.delete()

	@classmethod
	def create_product(cls,data):
		result = False
		message = None
		employee = Employee.objects.get(pk = data['pk_employee'])
		branch = employee.branch
		if data['excel'] == 1:
			cls.Delete_Product_All(cls, branch)
		try:
			product = cls.objects.get(branch = branch, code = data['code'])
			message = "Existo"
		except cls.DoesNotExist as e:
			message = str(e)
			product = None
		if product is None:
			try:
				product = cls(
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
				    branch= employee.branch,
				    subcategory= SubCategory.objects.get(pk = data['pk_subcategory']),
				    supplier = Supplier.objects.get(pk = data['pk_supplier'])
				)
				product.save()
				result = True
				message = "Success"
				info = serialized_employee = serializers.serialize('json', [employee])
				employee = json.loads(serialized_employee)
				History_Product.register_movement('Created', data, employee ,branch)
			except Exception as e:
				message = str(e)
		return {'result': result, 'message': message}

	@classmethod
	def update_product(cls, data):
		result = False
		message = None
		employee = Employee.objects.get(pk = data['pk_employee'])
		branch = employee.branch
		try:
			product = cls.objects.get(branch = branch, code = data['code'])
		except cls.DoesNotExist as e:
			message = str(e)
			product = None
		if product is not None:
			try:
				product.code = data['code']
				product.name = data['name']
				product.quantity = data['quantity']
				product.tax = data['tax']
				product.cost = data['cost']
				product.price_1 = data['price_1']
				product.price_2 = data['price_2']
				product.price_3 = data['price_3']
				product.ipo= data['ipo']
				product.discount = data['discount']
				product.branch = branch
				product.subcategory= SubCategory.objects.get(pk = data['pk_subcategory'])
				supplier = Supplier.objects.get(pk = data['pk_supplier'])
				product.save()
				result = True
				message = "Success"
				serialized_employee = serializers.serialize('json', [employee])
				employee = json.loads(serialized_employee)
				History_Product.register_movement('Modified', data, employee ,branch)
			except Exception as e:
				message = str(e)
		return {'result': result, 'message': message}

	@classmethod
	def delete_product(cls,data):
		result = False
		message = None
		employee = Employee.objects.get(pk = data['pk_employee'])
		branch = employee.branch
		try:
			_product = cls.objects.get(branch = branch, code = data['code'])
			message = "Existo"
			serialized_employee = serializers.serialize('json', [employee])
			employee = json.loads(serialized_employee)
			serialized_product = serializers.serialize('json', [_product])
			product = json.loads(serialized_product)[0]['fields']
			History_Product.register_movement('Deleted', product, employee ,branch)
			_product.delete()
			result = True
			message = 'Success'
		except cls.DoesNotExist as e:
			message = str(e)
			product = None
		return {'result':result, 'message':message}


	@classmethod
	def discount_product(cls,code, branch, quantity):
		result = False
		message = None
		try:
			product = cls.objects.get(code = code ,branch = branch)
			if product.quantity > 0:
				product.quantity -= quantity
				product.save()
			result = True
			message = "Success"
		except Exception as e:
			message = str(e)
		return {'result': result, 'message':message}

	@classmethod
	def get_list_products(cls, data):
		branch = Employee.objects.get(pk = data['pk_employee']).branch
		list_products = []
		for i in cls.objects.filter(branch = branch):
			product = serialized_employee = serializers.serialize('json', [i])
			list_products.append(json.loads(product)[0]['fields'])
		return list_products

	@classmethod
	def get_list_products_supplier(cls, data):
		branch = Employee.objects.get(pk = data['pk_employee']).branch
		list_products = []
		for i in cls.objects.filter(branch = branch, supplier = Supplier.objects.get(pk = data['pk_supplier'])):
			product = serialized_employee = serializers.serialize('json', [i])
			list_products.append(json.loads(product)[0]['fields'])
		return list_products


	@classmethod
	def get_product(cls, data):
		pk_employee = data['pk_employee']
		branch = Employee.objects.get(pk = data['pk_employee']).branch
		_product = cls.objects.get(branch = branch, code = data['code'])
		product = serialized_employee = serializers.serialize('json', [_product])
		data = json.loads(product)[0]['fields']
		data['pk_cat'] = SubCategory.objects.get(pk = data['subcategory']).category.pk
		data['category'] = SubCategory.objects.get(pk = data['subcategory']).category.name
		data['pk_subcategory'] = SubCategory.objects.get(pk = data['subcategory']).pk
		data['subcategory'] = SubCategory.objects.get(pk = data['subcategory']).name
		data['pk_supplier'] = Supplier.objects.get(pk = data['supplier']).pk
		data['supplier'] = Supplier.objects.get(pk = data['supplier']).name
		data['calculate_profit_percentages'] = cls.calculate_profit_percentages_one_quantity(_product)
		data['calculate_profit_amount'] = cls.calculate_profit_amount(_product)
		data['pk_category'] = data['pk_cat']
		data['list_subcategory'] = SubCategory.get_list_subcategory(data)
		data['pk_employee'] = pk_employee
		data['list_supplier'] = Supplier.list_supplier(data)
		return data


class History_Product(models.Model):
	ACTION_CHOICES = (
	    ('Created', 'Created'),
	    ('Modified', 'Modified'),
	    ('Deleted', 'Deleted')
	)
	action = models.CharField(max_length=10, choices=ACTION_CHOICES)
	product = models.JSONField()
	employee = models.JSONField()
	timestamp = models.DateTimeField(auto_now_add=True)
	branch = models.ForeignKey(Branch, on_delete = models.CASCADE, null = True, blank = True)

	def __str__(self):
		return f"{self.product.get('name', 'N/A')} - {self.action} by {self.employee[0]['fields']['user_name'].capitalize()} - {self.timestamp} "

	@classmethod
	def register_movement(cls, action, product, employee, branch):
		history_product = cls(
			action = action,
			product = product,
			employee = employee,
			branch = branch
		)
		history_product.save()


class Product_Reserved(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	user = models.ForeignKey(Employee, on_delete = models.CASCADE)

	@classmethod
	def reserveding_product(cls,data):
		user = Employee.objects.get(pk = data['pk_user'])
		product = Product.objects.get(code = data['pk_product'],branch = user.branch)
		result = False
		try:
			pr = cls.objects.get(product = product, user = user)
			pr.quantity += int(data['quantity'])
			pr.save()
		except cls.DoesNotExist as e:
			print(e)
			pr = None
		if pr is None:
			pr = cls(product= product, quantity= int(data['quantity']),user = user)
			pr.save()
			
		if product.quantity >= int(data['quantity']):
			product.quantity -= int(data['quantity'])
			try:
				product.save()
				result = True
			except Exception as e:
				print(e)
				pass
		return result


	@classmethod
	def return_products(cls,pk_user):
		pr = cls.objects.filter(user = Employee.objects.get(pk = pk_user))
		print(pr)
		for i in pr:
			p = Product.objects.get(pk = i.product.pk)
			p.quantity += i.quantity
			p.save()
			i.delete()
		return True

	@classmethod
	def return_product(cls, data):
		user = Employee.objects.get(pk = data['pk_employee'])
		product = Product.objects.get(code = data['pk_product'], branch = user.branch)		
		pr = cls.objects.get(product = product, user = user)
		pr.quantity += int(data['quantity'])
		product.quantity += int(data['quantity'])
		product.save()
		pr.save()
		if pr.quantity <= 0:
			pr.delete()
		return True

















