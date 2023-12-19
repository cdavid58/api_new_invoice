from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from django.db import IntegrityError
from django.db import models
from setting.models import *
import json, requests

class Company(models.Model):
	type_document_identification = models.ForeignKey(Type_Document_I, on_delete = models.CASCADE, null = True, blank = True)
	type_organization = models.ForeignKey(Type_Organization, on_delete = models.CASCADE, null = True, blank = True)
	type_regime = models.ForeignKey(Type_Regimen, on_delete = models.CASCADE, null = True, blank = True)
	municipality = models.ForeignKey(Municipalities, on_delete = models.CASCADE, null = True, blank = True)
	documentI = models.IntegerField(unique = True)
	name = models.CharField(max_length=200)
	address = models.CharField(max_length = 150)
	phone = models.CharField(max_length = 15)
	email = models.EmailField(unique=True)
	verified = models.BooleanField(default= False)
	production = models.BooleanField(default = False)
	token = models.CharField(max_length = 100, null = True, blank = True)
	logo = models.ImageField(upload_to = "Logo_Company", null = True, blank = True,default = "Logo_Company/withOut.png")

	def __str__(self):
		return self.name

	@staticmethod
	def dv(rut):
	    factores = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
	    rut_ajustado=str(rut).rjust( 15, '0')
	    s = sum(int(rut_ajustado[14-i]) * factores[i] for i in range(14)) % 11
	    if s > 1:
	        return 11 - s
	    else:
	        return s

	@staticmethod
	def create_company_api(cls,data):
		_url = Operation.objects.get(pk = 1).url_api
		url = f"{_url}/api/ubl2.1/config/{data['documentI']}/{cls.dv(data['documentI'])}"
		payload = json.dumps(data)
		headers = {
		  'Content-Type': 'application/json',
		  'Accept': 'application/json',
		  'Authorization': 'Bearer 7692a20fec92af0aa5729d796b019d27c83c9955407994630a0cdd7702ca2329'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		return json.loads(response.text)['token']

	@classmethod
	def create_company(cls,data):
		result = False
		message = None
		pk = None
		try:
			token = cls.create_company_api(cls,data)
			company = cls(
				documentI = data['documentI'],
				name = data['business_name'],
				address = data['address'],
				phone = data['phone'],
				email = data['email'],
				type_document_identification = Type_Document_I.objects.get(pk = data['type_document_identification_id']),
				type_organization = Type_Organization.objects.get(pk = data['type_organization_id']),
				type_regime = Type_Regimen.objects.get(pk = data['type_regime_id']),
				municipality = Municipalities.objects.get(pk = data['municipality_id']),
				token = token
			)
			company.save()
			result = True
			message = "Success"
			pk = company.pk
			data['pk_company'] = company.pk
			Branch.create_branch(data)
			result = Software.create_software(data,company)
		except IntegrityError as inte:
			Branch.create_branch(data)
			message = f"Error IntegrityError Company {inte}"
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message,'pk_company': pk}


class Branch(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length = 150)
	phone = models.CharField(max_length = 15)
	email = models.EmailField()
	verified = models.BooleanField(default= False)
	company = models.ForeignKey(Company, on_delete= models.CASCADE)
	psswd = models.CharField(max_length = 10,default = get_random_string(length=10))


	def __str__(self):
		return f"{self.name} - {self.company.name}"

	@classmethod
	def create_branch(cls,data):
		result = False
		message = None
		try:
			branch = cls(
				name = data['business_name'],
				address = data['address'],
				phone = data['phone'],
				email = data['email'],
				company = Company.objects.get(pk = data['pk_company'])
			)
			branch.save()
			result = True
			message = "Success"
			Resolution.create_resolution(data, branch)
			result = Consecutive.create_consecutive(branch)
			result = License.create_license(data, branch)
		except IntegrityError as inte:
			message = f"Error IntegrityError branch {inte}"
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}


class Resolution(models.Model):
	type_document_id = models.IntegerField()
	prefix = models.CharField(max_length = 7)
	resolution = models.IntegerField(null = True, blank = True)
	resolution_date = models.CharField(max_length = 10, null = True, blank = True)
	technical_key = models.CharField(max_length = 255, null = True, blank = True)
	_from = models.IntegerField()
	_to = models.IntegerField()
	generated_to_date = models.IntegerField(default = 0, null = True, blank = True)
	date_from = models.CharField(max_length = 10, null = True, blank = True)
	date_to = models.CharField(max_length = 10, null = True, blank = True)
	branch = models.ForeignKey(Branch, on_delete = models.CASCADE)

	@classmethod
	def get_resolution(cls, data):
		resolution = cls.objects.get(type_document_id = data['type_document'], branch = Branch.objects.get(pk = data['pk_branch']))
		return {'number': resolution._from, "prefix": resolution.prefix}

	@classmethod
	def add_number(cls, data):
		print(data)
		resolution = cls.objects.get(type_document_id = data['type_document'], branch = Branch.objects.get(pk = data['pk_branch']))
		result = False
		message = None
		if resolution._from <= resolution._to:
			resolution._from += 1
			resolution.save()
			result = True
			message = "Success"
		else:
			message = "Ya ha consumido todo el rango de numeración de su resolución, se le informa que debe generar otra resolución"
		return {'result':result, 'message':message}

	@classmethod
	def create_resolution(cls,data, branch):
		result = False
		message = None
		try:
			r = cls.objects.get(type_document_id = data['type_document_id'], branch = branch)
			r.type_document_id = data['type_document_id']
			r.prefix = data['prefix']
			r.resolution = data['resolution']
			r.resolution_date = data['resolution_date']
			r.technical_key = data['technical_key']
			r._from = data['from']
			r._to = data['to']
			r.date_from = data['date_from']
			r.date_to = data['date_to']
			result = True
			r.message = "Success"
			r.save()
		except cls.DoesNotExist as e:
			resolution = cls(
				type_document_id = data['type_document_id'],
				prefix = data['prefix'],
				resolution = data['resolution'],
				resolution_date = data['resolution_date'],
				technical_key = data['technical_key'],
				_from = data['from'],
				_to = data['to'],
				date_from = data['date_from'],
				date_to = data['date_to'],
				branch = branch,
			)
			resolution.save()
			result = True
			message = "Success"

		if result:
			result = cls.create_resolution_api(data, branch)
		return {'result':result, 'message':message}


	@staticmethod
	def create_resolution_api(data, branch):
		result = False
		message = None
		try:
			_url = Operation.objects.get(pk = 1).url_api
			url = f"{_url}/api/ubl2.1/config/resolution"
			payload = json.dumps(data)
			headers = {
			  'Content-Type': 'application/json',
			  'accept': 'application/json',
			  'Authorization': 'Bearer '+str(branch.company.token)
			}
			response = requests.request("PUT", url, headers=headers, data=payload)
			print(response.text)
			result = True
			message = "Success"
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}

	@classmethod
	def update_resolution(cls,data):
		result = False
		message = None
		try:
			resolution = cls.objects.get(type_document_id=data['type_document_id'], branch = data['pk_branch']) 
			resolution.type_document_id = data['type_document_id'],
			resolution.prefix = data['prefix']
			resolution.resolution = data['resolution']
			resolution.resolution_date = data['resolution_date']
			resolution.technical_key = data['technical_key']
			resolution._from = data['from']
			resolution._to = data['to']
			resolution.date_from = data['date_from']
			resolution.date_to = data['date_to']
			resolution.save()
			return cls.create_resolution_api(data, branch)
		except cls.DoesNotExist as e:
			message = str(e)
		return {'result': result, 'message': message}


class Software(models.Model):
	_id = models.CharField(max_length = 100)
	pin = models.IntegerField()
	company = models.ForeignKey(Company, on_delete = models.CASCADE)

	def __str__(self):
		return self.company.name

	@staticmethod
	def update_software_api(data,token):
		_url = Operation.objects.get(pk = 1).url_api
		url = f"{_url}/api/ubl2.1/config/software"
		payload = json.dumps(data)
		headers = {
		  'Content-Type': 'application/json',
		  'cache-control': 'no-cache',
		  'Connection': 'keep-alive',
		  'Accept-Encoding': 'gzip, deflate',
		  'accept': 'application/json',
		  'X-CSRF-TOKEN': '',
		  'Authorization': 'Bearer '+str(token)
		}
		response = requests.request("PUT", url, headers=headers, data=payload)
		return json.loads(response.text)["success"]

	@classmethod
	def create_software(cls,data,company):
		result = False
		message = None
		try:
			r = cls.update_software_api(data,company.token)
			print(r)
			if r:
				software = cls(
					_id = data['id'],
					pin = data['pin'],
					company = company
				)
				software.save()
				result = True
				message = "Success"
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}


class Consecutive(models.Model):
	pos = models.IntegerField(default = 1)
	elec = models.IntegerField(default = 1)
	nc = models.IntegerField(default = 1)
	nd = models.IntegerField(default = 1)
	ne = models.IntegerField(default = 1)
	ds = models.IntegerField(default = 1)
	hd = models.IntegerField(default = 1)
	branch = models.OneToOneField(Branch, on_delete = models.CASCADE, unique=True)

	def __str__(self):
		return self.branch.name

	@classmethod
	def create_consecutive(cls,branch):
		result = False
		message = None
		try:
			cls(branch = branch).save()
			result = True
			message = "Success"
		except IntegrityError as e:
			message = str(e)
		return {'result':result, 'message':message}

	@classmethod
	def consecutive_increment(cls,type_document):
		profit_percentages = {}
		
		consecutive = {
			'1': cls.pos,
			'2': cls.elec,
			'3': cls.nc,
			'4': cls.nd,
			'5': cls.ne,
			'6': cls.ds,
			'99': cls.hd
		}



		
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class License(models.Model):
	price = models.IntegerField(null = True, blank = True)
	document = models.IntegerField(null = True, blank = True)
	user = models.IntegerField(null = True, blank = True)
	branch = models.ForeignKey(Branch, on_delete = models.CASCADE, null = True, blank = True)
	date_registration = models.DateField(auto_now_add = True, null = True, blank = True)
	expiration_date = models.CharField(max_length = 12, null = True, blank = True)

	@staticmethod
	def packages(obj):
		data = {}
		if obj.price == 0:
			data = {
				'document':10,
				'user':1,
				'expiration_date': obj.date_registration  + timedelta(days=365)
			}
		elif obj.price == 18700:
			data = {
				'document':120,
				'user':1,
				'expiration_date': obj.date_registration  + relativedelta(months=1)
			}
		elif obj.price == 72500:
			data = {
				'document':120,
				'user':1,
				'expiration_date': obj.date_registration  + relativedelta(months=1)
			}
		elif obj.price == 168000:
			data = {
				'document':1500,
				'user':3,
				'expiration_date': obj.date_registration  + relativedelta(months=1)
			}
		elif obj.price == 191250:
			data = {
				'document':50000000,
				'user':5,
				'expiration_date': obj.date_registration  + relativedelta(months=1)
			}
		elif obj.price == 950000:
			data = {
				'document':50000000,
				'user':8,
				'expiration_date': obj.date_registration  + relativedelta(months=1)
			}
		return data

	@classmethod
	def create_license(cls, data, branch):
		result = False
		message = None
		try:
			license = cls(
				price = data['price']
			)
			license.save()
			p = cls.packages(license)
			license.document = p['document']
			license.user = p['user']
			license.branch = branch
			license.expiration_date = p['expiration_date']
			license.save()
			result = True
			message = "Success"
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}


	@classmethod
	def validate_date(cls,branch):
		license = cls.objects.get(branch = branch).expiration_date
		license_date  = datetime.strptime(license, '%Y-%m-%d')
		current_date = datetime.now()
		date_difference = license_date - current_date
		days_until_expiration = abs(date_difference.days)
		message = None
		result = False
		if date_difference.days < 0:
			message = "Su licencia esta expirada"
		else:
			result = True
			message = "Success"
		return {'result':result, 'message': message}
		


	@classmethod
	def add_user(cls,branch):
		result = False
		message = None
		try:
			license = cls.objects.get(branch = branch)
			license.user += 1
			license.save()
			result = True
			message = "Success"
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}

	@classmethod
	def discount_user(cls,branch):
		result = False
		message = None
		try:
			license = cls.objects.get(branch = branch)
			if license.user > 0:
				license.user -= 1
				license.save()
				result = True
				message = "Success"
			else:
				message = "Ya no tiene más usuarios disponibles"
		except Exception as e:
			print(e)
			message = str(e)
		return {'result':result, 'message':message}

	@classmethod
	def discount_license(cls, branch):
		result = False
		message = None
		try:
			license = cls.objects.get(branch = branch)
			if license.document > 0:
				license.document -= 1
				license.save()
				result = True
				message = "Success"
			else:
				message = "Ya no tiene más documentos electrónicos disponibles"
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}

	