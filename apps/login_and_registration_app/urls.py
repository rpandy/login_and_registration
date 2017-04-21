from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registration$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]
