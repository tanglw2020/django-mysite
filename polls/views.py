from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django import forms
from django.http import Http404

from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import time
import random
from pathlib import Path

from polls.forms import StudentForm
from polls.examModels import *
from polls.choiceQuestionModels import ChoiceQuestion
from polls.emailModels import EmailQuestion
from polls.fileOperationlModels import FileOperationQuestion
from polls.wordModels import WordQuestion
from polls.excelModels import ExcelQuestion
from polls.pptModels import PPTQuestion

import socket

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def exam_room(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        raise Http404("exam does not exist")
    
    exam_papers = exam.exampaper_set.all()
    # for exam_paper in exam_papers:
        # print(exam_paper.student, exam_paper.student.id)
    context = {
        'exam': exam,
        'exam_id': exam_id,
        'exam_papers': exam_papers,
        'login_url': 'http://'+get_host_ip()+':8000/exam/login',
        }
    return render(request, 'polls/exam_room_detail.html', context)



def login(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            # print(cleaned_data)

            # 查询用户是否在数据库中
            exam_id = cleaned_data['exam_id']
            student_id = cleaned_data['student_id']

            exam = Exam.objects.get(pk=exam_id)
            student = Student.objects.get(student_id=student_id)

            # 检查该考场和学号对应的试卷是否存在，不存在就创建新的试卷
            # 同时随机抽取题目
            choice_question_numb = exam.choice_question_num
            if not ExamPaper.objects.filter(student=student, exam=exam).exists():
                exam_paper = ExamPaper.objects.create(student=student, exam=exam)
                exam_paper.problem_type = exam.problem_type
                exam_paper.start_time = datetime.datetime.now()

                #########
                choice_questions_ids = [str(x['id']) for x in ChoiceQuestion.objects.values('id')]
                choice_questions_ids = random.sample(choice_questions_ids, choice_question_numb)
                exam_paper.choice_questions = ','.join(choice_questions_ids)
                exam_paper.choice_question_answers = ','.join(['+' for i in range(len(choice_questions_ids))])
                exam_paper.choice_question_results = ','.join(['0' for i in range(len(choice_questions_ids))])

                #########
                system_questions_ids = [str(x['id']) for x in FileOperationQuestion.objects.values('id')]
                exam_paper.system_operation_question =  random.sample(system_questions_ids, 1)[0]

                email_questions_ids = [str(x['id']) for x in EmailQuestion.objects.values('id')]
                exam_paper.email_question =  random.sample(email_questions_ids, 1)[0]
                
                questions_ids = [str(x['id']) for x in WordQuestion.objects.values('id')]
                exam_paper.word_question =  random.sample(questions_ids, 1)[0]
                
                questions_ids = [str(x['id']) for x in ExcelQuestion.objects.values('id')]
                exam_paper.excel_question =  random.sample(questions_ids, 1)[0]
                
                questions_ids = [str(x['id']) for x in PPTQuestion.objects.values('id')]
                exam_paper.ppt_question =  random.sample(questions_ids, 1)[0]
                
                exam_paper.save()
            else:
                exam_paper = ExamPaper.objects.get(student=student, exam=exam)

            return HttpResponseRedirect(reverse('exam:exampage', args=(exam_paper.id,)))
    else:
        form = StudentForm()

    context = {
        'form': form,
        }
    return render(request, 'polls/login.html', context)



@csrf_exempt
def api_download_scorelist(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        raise Http404("exam does not exist")

    exam_papers = exam.exampaper_set.all()
    line_head ="编号 班级 姓名 学号 选择题 编程题 总分"
    lines = [line_head]
    for i,exam_paper in enumerate(exam_papers):
        one_line = ' '.join([str(i), exam_paper.student.class_name, exam_paper.student.student_name, 
        exam_paper.student.student_id,
        str(exam_paper.choice_question_result_stat()).replace(' ',''),
        str(exam_paper.coding_question_result_detail()).replace(' ',''),
        str(exam_paper.total_score()) ])
        # print(one_line)
        lines.append(one_line)
    
    file_path = 'media/temp_scorelist/scorelist{}.txt'.format(exam_id)
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line+'\n')

    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="scorelist{}.txt"'.format(exam_id)
    return response
