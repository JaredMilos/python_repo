from django.conf.urls import url
from . import views 

urlpatterns = [
	url(r'^$', views.index),
    url(r'^register/$', views.register),
	url(r'^login/$', views.login),
	url(r'^wishes/$', views.wishes),
	url(r'^stats/$', views.stats),
	url(r'^(?P<wid>\d+)/edit_wish', views.edit_wish),
	url(r'^(?P<wid>\d+)/update', views.update),
	url(r'^(?P<wid>\d+)/destroy', views.destroy),
	url(r'^(?P<wid>\d+)/granted', views.granted),
	url(r'^(?P<wid>\d+)/like', views.like),
	url(r'^make_wish/$', views.make_wish),
	url(r'^wish/$', views.wish),
    url(r'^logout/$', views.logout)
]