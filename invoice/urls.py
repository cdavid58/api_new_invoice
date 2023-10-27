from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Create_Invoice/$',Create_Invoice,name="Create_Invoice"),
	url(r'^Create_Pass_Invoice/$',Create_Pass_Invoice,name="Create_Pass_Invoice"),
	url(r'^Cancel_All_Invoice/$',Cancel_All_Invoice,name="Cancel_All_Invoice"),
	url(r'^Get_List_Invoice/$',Get_List_Invoice,name="Get_List_Invoice"),
	url(r'^Annulled_Invoice/$',Annulled_Invoice,name="Annulled_Invoice"),
]