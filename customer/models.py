from setting.models import *
from django.db import models
from company.models import Branch
from user.models import Employee
from django.core import serializers
import json

class Customer(models.Model):
	identification_number = models.IntegerField()
	dv = models.IntegerField(default = 0)
	name = models.CharField(max_length = 100)
	phone = models.CharField(max_length = 12)
	address = models.CharField(max_length = 150)
	email = models.EmailField()
	type_document_i = models.ForeignKey(Type_Document_I, on_delete = models.CASCADE)
	type_organization = models.ForeignKey(Type_Organization, on_delete = models.CASCADE)
	municipality = models.ForeignKey(Municipalities, on_delete = models.CASCADE)
	type_regime = models.ForeignKey(Type_Regimen, on_delete = models.CASCADE)
	branch = models.ForeignKey(Branch, on_delete = models.CASCADE)

	def __str__(self):
		return f"{self.name} - {self.branch.name}"


	@staticmethod
	def dv_client(rut):
	    factores = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
	    rut_ajustado=str(rut).rjust( 15, '0')
	    s = sum(int(rut_ajustado[14-i]) * factores[i] for i in range(14)) % 11
	    if s > 1:
	        return 11 - s
	    else:
	        return s

	@classmethod
	def create_customer(cls, data):
		result = False
		message = None
		branch = Employee.objects.get(pk = data['pk_employee']).branch
		try:
			customer = cls.objects.get(identification_number = data['identification_number'], branch = branch)
			message = "The client already exists"
		except Exception as e:
			customer = cls(
				identification_number = data['identification_number'],
				dv = cls.dv_client(data['identification_number']),
				name = data['name'],
				phone = data['phone'],
				address = data['address'],
				email = data['email'],
				type_document_i = Type_Document_I.objects.get(pk = data['type_document_identification_id']),
				type_organization = Type_Organization.objects.get(pk = data['type_organization_id']),
				municipality = Municipalities.objects.get(pk = data['municipality_id']),
				type_regime = Type_Regimen.objects.get(pk = data['type_regime_id']),
				branch = branch
			)
			customer.save()
			result = True
			message = "Success"
		return {'result':result, 'message':message}

	@classmethod
	def get_list_customer(cls, data):
		branch = Employee.objects.get(pk = data['pk_employee']).branch
		list_customer = []
		for i in cls.objects.filter(branch = branch):
			serialized_customer = serializers.serialize('json', [i])
			list_customer.append(json.loads(serialized_customer)[0]['fields'])
		return list_customer


	@classmethod
	def get_customer(cls, data):
		branch = Employee.objects.get(pk = data['pk_employee']).branch
		serialized_customer = serializers.serialize('json', [cls.objects.get(identification_number = data['identification_number'], branch = branch)])
		return json.loads(serialized_customer)[0]['fields']
		
		