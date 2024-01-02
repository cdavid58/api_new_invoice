from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Create_Email/$',Create_Email,name="Create_Email"),
]