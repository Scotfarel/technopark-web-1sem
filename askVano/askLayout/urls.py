from django.urls import path

from . import views

urlpatterns = [
    path('question/', views.show_question, name='question'),
    path('ask/', views.show_ask, name='ask'),
    path('questions/', views.show_questions, name='questions'),
    path('base/', views.show_base, name='base'),
]
