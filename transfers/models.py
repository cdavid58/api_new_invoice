from django.db import models
from company.models import Branch
from inventory.models import Product, SubCategory, Supplier
from django.core import serializers
from django.http import JsonResponse
import json

class Transfer(models.Model):
	branch_sends = models.ForeignKey(Branch, on_delete= models.CASCADE, related_name="branch_sends")
	branch_receives = models.ForeignKey(Branch, on_delete= models.CASCADE, related_name="branch_receives")
	code = models.CharField(max_length= 150)
	product = models.CharField(max_length = 250)
	quantity = models.IntegerField()
	price = models.IntegerField()
	ipo = models.IntegerField()
	discount = models.IntegerField()

	@staticmethod
	def move_product(branch_sends, branch_receives, data):

	    _product = Product.objects.get(code=data['code'], branch=branch_sends)
	    try:
	        product = Product.objects.get(code=data['code'], branch=branch_receives)
	        product.quantity += data['quantity']
	        product.save()
	    except Product.DoesNotExist as e:
	        _data = json.loads(serializers.serialize('json', [_product]))[0]['fields']
	        _data.pop('id', None)
	        _data['branch'] = branch_receives
	        _data['subcategory'] = SubCategory.objects.get(pk = _data['subcategory'])
	        _data['supplier'] = Supplier.objects.filter(branch= branch_receives).first()
	        _data['quantity'] = data['quantity']
	        _data['price_1'] = data['price']
	        Product(**_data).save()
	    _product.quantity -= data['quantity']
	    _product.save()

	@staticmethod
	def get_branch(pk):
		return Branch.objects.get(pk = pk)

	@classmethod
	def transfer_products(cls, data):
		result = False
		message = None
		try:
			transfer = cls(
				branch_sends = Branch.objects.get(pk = data['branch_sends']),
				branch_receives = Branch.objects.get(pk = data['branch_receives']),
				code = data['code'],
				product = data['product'],
				quantity = data['quantity'],
				price = data['price'],
				ipo = data['ipo'],
				discount = data['discount']
			)
			transfer.save()
			cls.move_product(cls.get_branch(data['branch_sends']), cls.get_branch(data['branch_receives']), data)
			result = True
			message = "Success"
		except Exception as e:
			raise e
		return {'result':result, 'message':message}

