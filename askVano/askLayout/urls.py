from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.show_register, name='register'),
    path('login/', views.show_login, name='auth'),
    path('settings/', views.show_settings, name='settings'),
    path('tag/', views.show_tag, name='tag'),
    path('question/', views.show_question, name='question'),
    path('ask/', views.show_ask, name='ask'),
    path('questions/', views.show_questions, name='questions'),
    path('base/', views.show_base, name='base'),
]
