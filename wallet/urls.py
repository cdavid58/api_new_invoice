from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Get_List_Invoice_Credit/$',Get_List_Invoice_Credit,name="Get_List_Invoice_Credit"),
	url(r'^Get_Pass_Invoice/$',Get_Pass_Invoice,name="Get_Pass_Invoice"),
	url(r'^Get_Pass_Shopping/$',Get_Pass_Shopping,name="Get_Pass_Shopping"),
]