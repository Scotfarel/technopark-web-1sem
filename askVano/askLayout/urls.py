from django.urls import path, re_path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/(?P<page>\w+)/', views.show_index, name='index'),
    url(r'^index/', views.show_index, name='index'),
    url(r'^hot/(?P<page>\w+)/', views.show_hot, name='hot'),
    url(r'^hot', views.show_hot, name='hot'),
    url(r'^tag/(?P<id>\w+)/(?P<page>\w+)/', views.show_tag, name='tag'),
    url(r'^tag/(?P<id>\w+)/', views.show_tag, name='tag'),
    url(r'^question/$', views.show_question, name='question'),
    url(r'^question/(?P<id>\w+)/', views.show_question, name='question'),
    url(r'^login', views.show_login, name="login"),
    url(r'^logout', views.show_logout, name="logout"),
    url(r'^registration', views.show_registration, name="registration"),
    url(r'^ask', views.show_ask, name='ask'),
    url(r'^settings', views.show_settings, name='settings'),
]
