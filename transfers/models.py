from django.db import models
from company.models import Branch, Resolution ,License
from inventory.models import Product, SubCategory, Supplier
from django.core import serializers
from django.http import JsonResponse
import json

class Transfer(models.Model):
	branch_sends = models.ForeignKey(Branch, on_delete= models.CASCADE, related_name="branch_sends")
	branch_receives = models.ForeignKey(Branch, on_delete= models.CASCADE, related_name="branch_receives")
	number = models.IntegerField(max_length= 10, null=True, blank=True)
	note = models.TextField(null=True, blank=True)

	

	@classmethod
	def transfer_products(cls, data):
		result = False
		message = None
		try:
			branch = Branch.objects.get(pk = data['branch_sends'])
			transfer = cls(
				branch_sends = branch,
				branch_receives = Branch.objects.get(pk = data['branch_receives']),
				number = data['number'],
				note = data['notes']
			)
			transfer.save()
			if Details_Transfer.save_details(data, transfer):
				resolution = Resolution.objects.get(branch=branch, type_document_id = 98)
				resolution._from += 1
				resolution.save()
				License.discount_license(branch)
				print("Hola")
				message = "Success"
				result = True
		except Exception as e:
			raise e
		return {'result':result, 'message':message}


class Details_Transfer(models.Model):
	code = models.CharField(max_length= 150)
	product = models.CharField(max_length = 250)
	quantity = models.IntegerField()
	price = models.IntegerField()
	ipo = models.IntegerField()
	discount = models.IntegerField()
	transfer = models.ForeignKey(Transfer, on_delete = models.CASCADE)

	@staticmethod
	def move_product(branch_sends, branch_receives, data):
		result =False
		_product = Product.objects.get(code=data['code'], branch=branch_sends)
		if _product.quantity > 0:
		    try:
		        product = Product.objects.get(code=data['code'], branch=branch_receives)
		        product.quantity += int(data['quantity'])
		        product.save()
		    except Product.DoesNotExist as e:
		        _data = json.loads(serializers.serialize('json', [_product]))[0]['fields']
		        _data.pop('id', None)
		        _data['branch'] = branch_receives
		        _data['subcategory'] = SubCategory.objects.get(pk = _data['subcategory'])
		        _data['supplier'] = Supplier.objects.filter(branch= branch_receives).first()
		        _data['quantity'] = data['quantity']
		        _data['price_1'] = data['price_1']
		        Product(**_data).save()
		    _product.quantity -= int(data['quantity'])
		    _product.save()
		    result = True
		return result

	@staticmethod
	def get_branch(pk):
		return Branch.objects.get(pk = pk)

	@classmethod
	def save_details(cls, data, transfer):
		result = False
		for i in data['details']:
			cls(
				code = i['code'],
				product = i['name'],
				quantity = i['quantity'],
				price = i['price_1'],
				ipo = i['ipo'],
				discount = i['discount'],
				transfer = transfer
			).save()
			result = True
			result = cls.move_product(cls.get_branch(data['branch_sends']), cls.get_branch(data['branch_receives']), i)
		return result


