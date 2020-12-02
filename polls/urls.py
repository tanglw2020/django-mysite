
from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.login, name='index'),
    path('login', views.login, name='login'),
    path('examPage/<int:exam_id>/<int:student_id>', views.examPage, name='exampage'),
]
