from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Create_Shopping/$',Create_Shopping,name="Create_Shopping"),
	url(r'^Verified_Invoice/$',Verified_Invoice,name="Verified_Invoice"),
]