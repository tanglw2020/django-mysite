
from django.urls import path
from . import views

app_name = 'exam'
urlpatterns = [
    path('', views.index, name='index'),
]
