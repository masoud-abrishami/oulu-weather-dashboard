from django.urls import path
from weather.views import dashboard

urlpatterns = [path('', dashboard, name='dashboard')]
