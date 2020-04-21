from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'about', views.show_base, name='base'),
    re_path(r'signup', views.show_register, name='signup'),
    re_path(r'login', views.show_login, name='auth'),
    re_path(r'settings', views.show_settings, name='settings'),
    re_path(r'tag', views.show_tag, name='tag'),
    re_path(r'hot', views.show_hot, name='hot'),
    re_path(r'question', views.show_question, name='question'),
    re_path(r'ask', views.show_ask, name='ask'),
    path('', views.show_questions, name='questions'),
    re_path(r'base', views.show_base, name='base'),
    re_path(r'(?P<question_id>[0-9]+)$', views.show_question, name='question'),
    path('questions/<int:question_id>/', views.show_question, name='question'),
]
