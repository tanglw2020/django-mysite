
from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('set_word_operation', views.set_word_operation, name='set_word_operation'),
    path('add_word_question', views.add_word_question, name='add_word_question'),
    path('add_excel_question', views.add_excel_question, name='add_excel_question'),
    path('add_ppt_question', views.add_ppt_question, name='add_ppt_question'),
    path('add_choice_question', views.add_choice_question, name='add_choice_question'),
    path('scan_question', views.scan_question, name='scan_question'),
]
