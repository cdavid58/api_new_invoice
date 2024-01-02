from user.models import Employee
from django.db import models
import json, base64, tempfile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class Emails(models.Model):
	sender = models.ForeignKey(Employee, on_delete= models.CASCADE, related_name="envia")
	receives = models.ForeignKey(Employee, on_delete= models.CASCADE, related_name="recibe")
	subject = models.CharField(max_length= 255, null = True, blank= True)
	message = models.TextField()

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