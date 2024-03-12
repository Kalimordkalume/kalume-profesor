from django.urls import path
from . import views

app_name = 'calculator'
urlpatterns = [
    path("",views.EnergyView.as_view() ,name='calculator_home'),
    
]
