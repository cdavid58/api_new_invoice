from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Create_Email/$',Create_Email,name="Create_Email"),
	url(r'^Get_List_Emails/$',Get_List_Emails,name="Get_List_Emails"),
	url(r'^Is_Read/$',Is_Read,name="Is_Read"),
]