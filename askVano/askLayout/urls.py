from django.urls import path

from . import views

urlpatterns = [
    path('base/', views.show_base, name='base'),
]
