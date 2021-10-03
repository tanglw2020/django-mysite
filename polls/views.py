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
import socket
from zipfile import ZipFile
from pathlib import Path

from polls.forms import *
from polls.examModels import *
from polls.choiceQuestionModels import ChoiceQuestion
from polls.emailModels import EmailQuestion
from polls.fileOperationlModels import FileOperationQuestion
from polls.wordModels import WordQuestion
from polls.excelModels import ExcelQuestion
from polls.pptModels import PPTQuestion

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'

def handle_uploaded_file(f, output_save_path):
    # print(os.path.join(root_path,filename))
    with open(output_save_path, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def exampage(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('exam:login'))

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'choice_questions_answers': exam_page.choice_question_answers_(),
        }
    return render(request, 'polls/exam_page.html', context)


def exampage(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('exam:login'))

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'choice_questions_answers': exam_page.choice_question_answers_(),
        }
    return render(request, 'polls/exam_page.html', context)

def exampage_choice_question(request, exampage_id, choice_question_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('exam:login'))

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'choice_questions_answers': exam_page.choice_question_answers_(),
        'choice_question': exam_page.choice_questions_pk_(choice_question_id),
        'choice_question_id': choice_question_id,
        }
    return render(request, 'polls/exam_page_choice_question.html', context)


def exampage_email_question(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('exam:login'))

    uploadsucc = False
    email_question = exam_page.email_questions_pk_()
    if request.method == 'POST':
        form = SendEmailForm(request.POST, request.FILES)
        if form.is_valid():
            uploadsucc = True
            cleaned_data = form.cleaned_data
            # print(cleaned_data)
            score = 0
            if cleaned_data['name1'] == email_question.des_name: score = score + 1
            if cleaned_data['name2'] == email_question.cop_name: score = score + 1
            if cleaned_data['topic'] == email_question.topic: score = score + 1
            if cleaned_data['content'] == email_question.content: score = score + 1
            exam_page.email_result = exam_page.exam.email_score * score / 4
            exam_page.email_answer = cleaned_data['topic']+':'+cleaned_data['content']
            exam_page.save()
    else:
        form = SendEmailForm()

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'email_question': email_question,
        'form': form,
        'uploadsucc': uploadsucc,
        }
    return render(request, 'polls/exam_page_email_question.html', context)


def exampage_system_question(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('exam:login'))

    uploadsucc = False
    system_question = exam_page.system_questions_pk_()
    if request.method == 'POST':
        form = UploadZipFileForm(request.POST, request.FILES)
        if form.is_valid():
            output_save_path = exam_page.system_operation_answer_save_path_()
            if os.path.exists(output_save_path): shutil.rmtree(output_save_path)
            os.makedirs(output_save_path)

            output_save_file = os.path.join(output_save_path, 'files.zip')
            handle_uploaded_file(request.FILES['file'], output_save_file)

            with ZipFile(output_save_file) as myzip:
                myzip.extractall(output_save_path)

            exam_page.system_operation_answer = output_save_file
            results = system_question.score_(os.path.join(output_save_path, 'exam_system_operation'))
            if len(results)==0:
                exam_page.system_operation_result = 0
            else:
                corrects_ = [x for x in results if x]
                exam_page.system_operation_result = exam_page.exam.file_operation_score * len(corrects_) / len(results)
            print(exam_page.system_operation_result)
            exam_page.save()
            
            uploadsucc = True
    else:
        form = UploadZipFileForm()

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'system_question': system_question,
        'form': form,
        'uploadsucc': uploadsucc,
        }
    return render(request, 'polls/exam_page_system_question.html', context)


def exampage_word_question(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('exam:login'))
    
    uploadsucc = False
    word_question = exam_page.word_questions_pk_()
    if request.method == 'POST':
        form = UploadWordForm(request.POST, request.FILES)
        if form.is_valid():
            output_save_path = exam_page.word_answer_save_path_()
            if os.path.exists(output_save_path): shutil.rmtree(output_save_path)
            os.makedirs(output_save_path)

            output_save_file = os.path.join(output_save_path, 'word.docx')
            handle_uploaded_file(request.FILES['file'], output_save_file)

            exam_page.word_answer = output_save_file
            exam_page.word_result = exam_page.exam.word_score * word_question.score_(output_save_file)
            exam_page.save()
            
            uploadsucc = True
    else:
        form = UploadWordForm()

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'word_question': word_question,
        'form': form,
        'uploadsucc': uploadsucc,
        }
    return render(request, 'polls/exam_page_word_question.html', context)


def exampage_excel_question(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('exam:login'))

    uploadsucc = False
    excel_question = exam_page.excel_questions_pk_()
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            output_save_path = exam_page.excel_answer_save_path_()
            if os.path.exists(output_save_path): shutil.rmtree(output_save_path)
            os.makedirs(output_save_path)

            output_save_file = os.path.join(output_save_path, 'excel.xlsx')
            handle_uploaded_file(request.FILES['file'], output_save_file)

            exam_page.excel_answer = output_save_file
            _, score = excel_question.score_(output_save_file)
            exam_page.excel_result = exam_page.exam.excel_score * score
            exam_page.save()
            
            uploadsucc = True
    else:
        form = UploadExcelForm()

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'excel_question': excel_question,
        'form': form,
        'uploadsucc': uploadsucc,
        }
    return render(request, 'polls/exam_page_excel_question.html', context)


def exampage_ppt_question(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('exam:login'))

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        }
    return render(request, 'polls/exam_page_ppt_question.html', context)


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
        raise Http404("exam {} does not exist".format(exam_id))
    
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


@csrf_exempt
def api_get_server_time(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')

    diff = int(timezone.now().timestamp() - exam_page.start_time.timestamp())
    a = {}
    a["result"] = str(int(diff/60))+'分钟'+str(diff%60)+'秒'  ##"post_success"
    return HttpResponse(json.dumps(a), content_type='application/json')


@csrf_exempt
def api_handle_choice_answer(request, exampage_id, choice_question_id, choice_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    # old_answers = exam_page.choice_question_answers.split(',')
    # old_answers[choice_question_id-1] = str(choice_id)
    # exam_page.choice_question_answers = ','.join(old_answers)
    # exam_page.save()
    exam_page.update_choice_question_answer_result_(choice_question_id, choice_id)
    a = {}
    return HttpResponse(json.dumps(a), content_type='application/json')


@csrf_exempt
def api_download_system_zipfile(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    
    system_question = exam_page.system_questions_pk_()

    file_path = system_question.zipfile_path_()
    if file_path:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="operation-system.zip"'
        return response
    else:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')



@csrf_exempt
def api_download_word_zipfile(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    
    word_question = exam_page.word_questions_pk_()
    file_path = word_question.zip_path_()
    if file_path:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="word.zip"'
        return response
    else:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')


@csrf_exempt
def api_download_excel_zipfile(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    
    question = exam_page.excel_questions_pk_()
    file_path = question.zip_path_()
    if file_path:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="excel.zip"'
        return response
    else:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')


@csrf_exempt
def api_download_ppt_zipfile(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(id=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    
    question = exam_page.ppt_questions_pk_()
    file_path = question.zip_path_()
    if file_path:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="ppt.zip"'
        return response
    else:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')