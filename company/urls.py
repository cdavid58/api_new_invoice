from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Create_Company/$',Create_Company,name="Create_Company"),
	url(r'^Create_Resolution/$',Create_Resolution,name="Create_Resolution"),
]