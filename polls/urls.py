
from django.urls import path
from . import views

app_name = 'exam'
urlpatterns = [
    path('login', views.login, name='login'),
    path('exampage/<int:exampage_id>', views.exampage, name='exampage'),
    path('exampage/<int:exampage_id>/choicequestion/<int:choice_question_id>', views.exampage_choice_question, name='exampage-choicequestion'),
    path('exampage/<int:exampage_id>/emailquestion/', views.exampage_email_question, name='exampage-emailquestion'),
    path('exampage/<int:exampage_id>/systemquestion/', views.exampage_system_question, name='exampage-systemquestion'),
    path('exampage/<int:exampage_id>/wordquestion/', views.exampage_word_question, name='exampage-wordquestion'),
    path('exampage/<int:exampage_id>/excelquestion/', views.exampage_excel_question, name='exampage-excelquestion'),
    path('exampage/<int:exampage_id>/pptquestion/', views.exampage_ppt_question, name='exampage-pptquestion'),
    path('room/<int:exam_id>', views.exam_room, name='examroom'),
    path('api/download/scorelist<int:exam_id>.txt', views.api_download_scorelist, name='api-download-scorelist'),
    path('api/getservertime/<int:exampage_id>', views.api_get_server_time,name='api-getservertime'),
    path('api/sendchoiceanswer/<int:exampage_id>/<int:choice_question_id>/<int:choice_id>', views.api_handle_choice_answer,name='api-choiceanswer'),
    path('api/download/systemzip/<int:exampage_id>', views.api_download_system_zipfile, name='api-download-system-zipfile'),
]
