from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Create_Employee/$',Create_Employee,name="Create_Employee"),
	url(r'^Login/$',Login,name="Login"),
]