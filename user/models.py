from django.utils.crypto import get_random_string
from django.db import models
from company.models import Branch
from setting.models import *
from django.core import serializers
from django.http import JsonResponse
import json, env

class Employee(models.Model):
    type_worker_id = models.ForeignKey(Type_Worker, on_delete = models.CASCADE)
    sub_type_worker_id = models.ForeignKey(Sub_Type_Worker, on_delete = models.CASCADE)
    payroll_type_document_identification_id = models.ForeignKey(Payroll_Type_Document_Identification, on_delete = models.CASCADE)
    municipality_id = models.ForeignKey(Municipalities, on_delete = models.CASCADE)
    type_contract_id = models.ForeignKey(Type_Contract, on_delete = models.CASCADE)
    high_risk_pension = models.BooleanField()
    identification_number = models.IntegerField()
    surname = models.CharField(max_length=255)
    second_surname = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255)
    integral_salary = models.BooleanField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    branch = models.ForeignKey(Branch, on_delete = models.CASCADE, null = True, blank = True)
    user_name = models.CharField(max_length = 20, null = True, blank = True,unique=True)
    psswd = models.CharField(max_length = 20,default = get_random_string(length=20), unique = True)
    block = models.BooleanField(default = False)
    login_attempts = models.PositiveIntegerField(default=0)
    permission = models.ManyToManyField(Permission, blank = True, null = True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"

    @classmethod
    def login(cls, data):
        result = False
        message = None
        try:
            employee = cls.objects.get(user_name=data['user_name'].lower(), psswd= data['psswd'])
        except cls.DoesNotExist as e:
            message = str(e)
            employee = None
        data = {'result':result, 'message':message}
        if employee is not None:
            result = True
            message = "Success"
            data = {
                'result':result, 'message':message, 'pk_employee': employee.pk, 'name': f"{employee.first_name} {employee.surname}",
                "pk_branch":employee.branch.pk, "name_branch": employee.branch.name, 'logo': env.URL_LOCAL + employee.branch.company.logo.url
            }
            data['permission'] = [ i.name for i in employee.permission.all()]
        return data




    @classmethod
    def create_employee(cls, data):
        result = False
        message = None
        try:
            employee = cls.objects.get(identification_number=data['identification_number'])
            message = "The employee already exists."
        except cls.DoesNotExist as e:
            employee = None

        if employee is None:
            employee = cls(
                type_worker_id = Type_Worker.objects.get(id = data['type_worker_id']),
                sub_type_worker_id = Sub_Type_Worker.objects.get(id = data['sub_type_worker_id']),
                payroll_type_document_identification_id = Payroll_Type_Document_Identification.objects.get(id = data['payroll_type_document_identification_id']),
                municipality_id = Municipalities.objects.get(id = data['municipality_id']),
                type_contract_id = Type_Contract.objects.get(id = data['type_contract_id']),
                high_risk_pension = data['high_risk_pension'],
                identification_number = data['identification_number'],
                surname = data['surname'],
                second_surname = data['second_surname'],
                first_name = data['first_name'],
                middle_name = data['middle_name'],
                address = data['address'],
                integral_salary = data['integral_salary'],
                salary = data['salary'],
                email = data['email'],
                branch = cls.objects.get(pk = data['pk_user']).branch,
                user_name = data['user_name'].lower(),
                psswd = get_random_string(length=20) if data['psswd'] is None else data['psswd']
            )
            employee.save()
            result = True
            for i in data['permission']:
                employee.permission.add(Permission.objects.get(_id = i))
            message = "Success"
            _data = json.loads(cls.get_employee_serialized(data['pk_user']).content.decode('utf-8'))[0]['fields']
            History_Employee.register_movement("Created",_data,data)

        return {'result':result, 'message':message}

    @staticmethod
    def get_employee_serialized(employee_id):
        try:
            employee = Employee.objects.get(pk=employee_id)
            serialized_employee = serializers.serialize('json', [employee])
            return JsonResponse(json.loads(serialized_employee), safe=False)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Empleado no encontrado'}, status=404)

class History_Employee(models.Model):
    ACTION_CHOICES = (
        ('Created', 'Created'),
        ('Modified', 'Modified'),
        ('Deleted', 'Deleted')
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, null = True, blank = True)
    user_who_registers = models.JSONField(null = True, blank = True)
    recorded_user = models.JSONField(null = True, blank = True)
    timestamp = models.DateTimeField(auto_now_add = True, null = True, blank = True)

    @classmethod
    def register_movement(cls,action,uwr, ru):
        cls(
            action = action,
            user_who_registers = uwr,
            recorded_user = ru
        ).save()












