from django.urls import path
from .views import subnet_calculator

urlpatterns = [
    path('', subnet_calculator, name='subnet_calculator'),
]
