from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Create_Customer/$',Create_Customer,name="Create_Customer"),
	url(r'^Get_List_Customer/$',Get_List_Customer,name="Get_List_Customer"),
	url(r'^Get_Customer/$',Get_Customer,name="Get_Customer"),
]