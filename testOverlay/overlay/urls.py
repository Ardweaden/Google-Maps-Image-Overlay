from django.urls import path
from django.contrib.auth import logout
from . import views

app_name = 'overlay'
urlpatterns = [
        path('',views.index,name='index')
        ]