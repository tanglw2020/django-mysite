
from django.urls import path
from . import views

app_name = 'exam'
urlpatterns = [
    path('', views.login, name='login'),
    path('loginsecond', views.login_second, name='login-second'),
    path('exampage/u76ggj8j9-12-2234688-398749-828-<exampage_id>201-9239-21nhymsjksealjlfdkja', views.exampage, name='exampage'),
    path('exampage/-khgtgg543fjk-dfd568-7989<exampage_id>201nhymsjksealjlfdkja/choicequestion/<int:choice_question_id>', views.exampage_choice_question, name='exampage-choicequestion'),
    path('exampage/hgoiugiugoi-dfd568-7989<exampage_id>201nhymsjksealjlfdkja/textquestion/', views.exampage_text_question, name='exampage-textquestion'),
    path('exampage/dfd568-7989<exampage_id>201nhymsjksealjlfdkja/emailquestion/', views.exampage_email_question, name='exampage-emailquestion'),
    path('exampage/gj8j9-khgtggiugoi-df989<exampage_id>201nhymsjksealjlfdkja/systemquestion/', views.exampage_system_question, name='exampage-systemquestion'),
    path('exampage/u76gugiugoi-dfd568-7989<exampage_id>201nhymsjksealjlfdkja/wordquestion/', views.exampage_word_question, name='exampage-wordquestion'),
    path('exampage/u76ggjgiugoi--7989<exampage_id>201nhymsjksealjlfdkja/excelquestion/', views.exampage_excel_question, name='exampage-excelquestion'),
    path('exampage/tgg543fjk-hgoi568-7989<exampage_id>201nhymsjksealjlfdkja/pptquestion/', views.exampage_ppt_question, name='exampage-pptquestion'),
    path('room/I-1iak_sdo123pf37lkn==Yl234kf1e4<int:exam_id>21oio32874ia78412j765s98fuo', views.exam_room, name='examroom'),
    path('api/download/scorelist<int:exam_id>.xlsx', views.api_download_scorelist_xlsx, name='api-download-scorelist'),
    path('api/getservertime/<exampage_id>', views.api_get_server_time,name='api-getservertime'),
    path('api/sendchoiceanswer/<exampage_id>/<int:choice_question_id>/<int:choice_id>', views.api_handle_choice_answer,name='api-choiceanswer'),
    path('api/download/systemzip/<exampage_id>', views.api_download_system_zipfile, name='api-download-system-zipfile'),
    path('api/download/wordzip/<exampage_id>', views.api_download_word_zipfile, name='api-download-word-zipfile'),
    path('api/download/excelzip/<exampage_id>', views.api_download_excel_zipfile, name='api-download-excel-zipfile'),
    path('api/download/pptzip/<exampage_id>', views.api_download_ppt_zipfile, name='api-download-ppt-zipfile'),
    path('api/submitall/<exampage_id>', views.api_submit_all, name='api-submit-all'),
    path('api/addtime/<exampage_id>', views.add_time_enable, name='api-addtime'),
]
