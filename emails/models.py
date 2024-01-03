from user.models import Employee
from django.db import models
import json, base64, tempfile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.core import serializers
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

class Emails(models.Model):
	sender = models.ForeignKey(Employee, on_delete= models.CASCADE, related_name="envia")
	receives = models.ForeignKey(Employee, on_delete= models.CASCADE, related_name="recibe")
	subject = models.CharField(max_length= 255, null = True, blank= True)
	message = models.TextField()
	date_register = models.DateTimeField(auto_now_add= True, null = True, blank= True)
	is_read_email = models.BooleanField(default= False, blank=True, null=True)

	@staticmethod
	def Calculate_Value(Time):
		fecha_dada = datetime.strptime(Time, "%Y-%m-%dT%H:%M:%S.%f")
		fecha_dada = fecha_dada.replace(tzinfo=timezone.utc)
		fecha_actual = datetime.now(timezone.utc)
		diferencia = fecha_actual - fecha_dada
		diferencia -= timedelta(hours=5)
		diferencia_relativa = relativedelta(fecha_actual, fecha_dada)
		anos = diferencia_relativa.years
		meses = diferencia_relativa.months
		dias = diferencia.days
		segundos_totales = diferencia.seconds
		horas, segundos = divmod(segundos_totales, 3600)
		minutos, segundos = divmod(segundos, 60)

		message = None
		if anos > 0:
		    message = f"Hace {anos} {'año' if anos == 1 else 'años'}."
		elif meses > 0:
		    message = f"Hace {meses} {'mes' if meses == 1 else 'meses'}."
		elif dias > 0:
		    message = f"Hace {dias} {'día' if dias == 1 else 'días'}."
		elif horas > 0:
		    message = f"Hace {horas} {'hora' if horas == 1 else 'horas'}."
		elif minutos > 0:
		    message = f"Hace {minutos} {'minuto' if minutos == 1 else 'minutos'}."
		else:
		    message = "Hace menos de un minuto."
		return message

	@classmethod
	def is_read(cls, data):
		email = cls.objects.get(pk = data['pk_email'])
		email.is_read_email = data['is_read']
		email.save()
		return {'result':True}

	@classmethod
	def create_email(cls, data):
		result = False
		message = None
		try:
			email = cls(
				sender = Employee.objects.get(pk = data['sender']),
				receives = Employee.objects.get(pk = data['receives']),
				subject = data['subject'],
				message = data['message']
			)
			email.save()
			message = "Success"
			result = True
			if len(data['files']) > 0:
				return Attached_Files.save_files(data,email)
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message}


	@classmethod
	def get_list_emails(cls, data):
		result = False
		message = None
		_data = []
		try:
			employee = Employee.objects.get(pk = data['pk_employee'])
			for i in cls.objects.filter(Q(sender=employee) | Q(receives=employee)).order_by('-date_register'):
				_value = json.loads( serializers.serialize('json', [i] ))[0]
				_value['fields']['diferencia'] = cls.Calculate_Value(_value['fields']['date_register'])
				_data.append(_value)
			result = True
			message = "Success"
		except Exception as e:
			message = str(e)
		return {'result':result, 'message':message, 'data':_data}

class Attached_Files(models.Model):
	email = models.ForeignKey(Emails, on_delete = models.CASCADE)
	file = models.FileField(upload_to= "files_emails")

	def __str__(self):
		return f"{self.email.subject} - {self.email.receives.first_name} {self.email.receives.first_name}  by {self.email.sender.first_name} {self.email.sender.first_name} ----- {self.email.sender.branch.name}"

	@classmethod
	def save_files(cls, data, email):
		result = False
		message = None
		try:
		    for i in data.get('files', []):
		        try:
		            file_data = base64.b64decode(i.get('base_64', ''))
		            file_name = i.get('name_file', 'unknown_file')
		            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
		                temp_file.write(file_data)
		            saved_file_path = default_storage.save(file_name, ContentFile(file_data))
		            file_instance = cls(
		                email=email,
		                file=saved_file_path
		            )
		            file_instance.save()
		            result = True
		            message = "Success"
		        except Exception as e:
		            message = str(e)
		            result = False
		except Exception as e:
		    message = str(e)
		return {'result': result, 'message': message}