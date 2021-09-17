from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
from polls.choiceQuestionModels import *



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
