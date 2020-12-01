from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from .forms import StudentForm
from .studentModels import Student
from .examModels import Exam

def index(request):
    action_list = [
    ("查看题库", '/polls/scan_question'),
    ("录入选择题",'/polls/add_choice_question'),
    ("录入word操作题",'/polls/add_word_question'),
    ("录入Excel操作题",'/polls/add_excel_question'),
    ("录入PPT操作题",'/polls/add_ppt_question'),
    ]
    context = {'action_list': action_list}
    return render(request, 'polls/index.html', context)


def login(request):

    if request.method == 'POST':
        # 如果登录成功，绑定参数到cookie中，set_cookie
        form = StudentForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            # print(cleaned_data)

            # 查询用户是否在数据库中
            exam_id = cleaned_data['exam_id']
            student_id = cleaned_data['student_id']
            name = cleaned_data['name']
            class_name = cleaned_data['class_name']

            exam = Exam.objects.get(id=exam_id)
            student_set = exam.student_set.all()
            if student_set.filter(student_id=student_id).exists():
                # user = student_set.get(student_id=student_id)
                return HttpResponseRedirect(reverse('polls:exampage', args=(exam_id, student_id)))
            else:
                student_set.create( exam_info_id=exam_id,
                                    class_name = class_name,
                                    name = name, 
                                    student_id = student_id)
                return HttpResponseRedirect(reverse('polls:exampage', args=(exam_id, student_id)))
                # return HttpResponse('添加: '+ str(student_id))
    else:
        form = StudentForm()

    context = {
        'form': form,
        }
    return render(request, 'polls/login.html', context)

def examPage(request, exam_id, student_id):
    return HttpResponse('考试:{} 学号:{} '.format(exam_id, student_id))
    