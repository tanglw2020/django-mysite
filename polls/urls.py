
from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('input_word_operation', views.input_word_operation, name='input_word_operation'),
    path('', views.index, name='index'),
]
