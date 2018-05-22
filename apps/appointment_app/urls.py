from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^appointments$', views.appointments),
    url(r'^appointments/(?P<appointment_id>\d+)$', views.edit),
    url(r'^add$', views.add),
    url(r'^delete/(?P<appointment_id>\d+)$', views.delete),
    url(r'^update/(?P<appointment_id>\d+)$', views.update)
]