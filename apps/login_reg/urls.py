from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^travels$', views.travels),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^post_add$', views.post_add),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^destination/(?P<trip_id>\d+)$', views.destination),
]
