from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^login', views.show_login, name="login"),
    re_path(r'^logout', views.show_logout, name="logout"),
    re_path(r'^registration', views.show_registration, name="registration"),
    re_path(r'^settings', views.show_settings, name='settings'),

    re_path(r'^ask', views.show_ask, name='ask'),
    re_path(r'^index/(?P<page>\w+)/', views.show_index, name='index'),
    re_path(r'^index/', views.show_index, name='index'),
    re_path(r'^hot/(?P<page>\w+)/', views.show_hot, name='hot'),
    re_path(r'^hot', views.show_hot, name='hot'),
    re_path(r'^tag/(?P<id>\w+)/(?P<page>\w+)/', views.show_tag, name='tag'),
    re_path(r'^tag/(?P<id>\w+)/', views.show_tag, name='tag'),

    re_path(r'^question/(?P<id>\w+)/', views.show_question, name='question'),
]

