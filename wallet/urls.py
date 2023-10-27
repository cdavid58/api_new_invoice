from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Get_List_Invoice_Credit/$',Get_List_Invoice_Credit,name="Get_List_Invoice_Credit"),
]