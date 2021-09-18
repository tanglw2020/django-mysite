
from django.urls import path
from . import views

app_name = 'exam'
urlpatterns = [
    path('login', views.login, name='login'),
    path('exampage/<int:exampage_id>', views.exampage, name='exampage'),
    path('room/<int:exam_id>', views.exam_room, name='examroom'),
    path('api/download/scorelist<int:exam_id>.txt', views.api_download_scorelist, name='api-download-scorelist'),
    path('api/getservertime/<int:exampage_id>', views.api_get_server_time,name='api-getservertime'),
]
