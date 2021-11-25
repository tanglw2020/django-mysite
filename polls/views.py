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
from polls.textinputModels import TextQuestion

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'

def handle_uploaded_file(f, output_save_path):
    # print(os.path.join(root_path,filename))
    with open(output_save_path, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def exampage(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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


def exampage_text_question(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('exam:login'))

    uploadsucc = False
    text_question = exam_page.text_questions_pk_()
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            uploadsucc = True
            cleaned_data = form.cleaned_data
            # print(cleaned_data)
            exam_page.text_question_result = round(exam_page.exam.text_score * text_question.score_(cleaned_data['content']), 1)
            exam_page.text_question_answer = json.dumps(cleaned_data)
            exam_page.save()
    else:
        if exam_page.text_question_answer:
            cleaned_data = json.loads(exam_page.text_question_answer)
            form = TextInputForm(cleaned_data)
        else:
            form = TextInputForm()

    if not exam_page.enabled:
        form.fields['content'].widget.attrs['readonly'] = True
        # form.fields['content'].widget.attrs['unselectable'] = "on"

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'text_question': text_question,
        'form': form,
        'uploadsucc': uploadsucc,
        }
    return render(request, 'polls/exam_page_text_question.html', context)


def exampage_email_question(request, exampage_id):
    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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
            exam_page.email_result = round(exam_page.exam.email_score * score / 4, 1)
            # exam_page.email_answer = cleaned_data['name1']+'\n'+cleaned_data['name2']+'\n'+cleaned_data['topic']+'\n'+cleaned_data['content']
            exam_page.email_answer = json.dumps(cleaned_data)
            exam_page.save()
    else:
        cleaned_data = {}
        if exam_page.email_answer:
            cleaned_data = json.loads(exam_page.email_answer)
            form = SendEmailForm(cleaned_data)
        else:
            form = SendEmailForm()

    if not exam_page.enabled:
        form.fields['name1'].widget.attrs['readonly'] = True
        form.fields['name2'].widget.attrs['readonly'] = True
        form.fields['topic'].widget.attrs['readonly'] = True
        form.fields['content'].widget.attrs['readonly'] = True

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
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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

            # with ZipFile(output_save_file) as myzip:
            #     myzip.extractall(output_save_path)

            exam_page.system_operation_answer = output_save_file
            exam_page.system_operation_submit_cnt = str(int(exam_page.system_operation_submit_cnt)+1)
            results = system_question.score_zip_(output_save_file)
            if len(results)==0:
                exam_page.system_operation_result = 0
            else:
                corrects_ = [x for x in results if x]
                exam_page.system_operation_result = round(exam_page.exam.file_operation_score * len(corrects_) / len(results), 1)
            # print(exam_page.system_operation_result)
            exam_page.save()
            
            uploadsucc = True
    else:
        form = UploadZipFileForm()

    if not exam_page.enabled:
        form.fields['file'].widget.attrs['disabled'] = True

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
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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

            exam_page.word_submit_cnt = str(int(exam_page.word_submit_cnt)+1)
            exam_page.word_answer = output_save_file
            exam_page.word_result = round(exam_page.exam.word_score * word_question.score_(output_save_file), 1)
            # print('word_result:', exam_page.exam.word_score, word_question.score_(output_save_file))
            exam_page.save()
            
            uploadsucc = True
    else:
        form = UploadWordForm()

    if not exam_page.enabled:
        form.fields['file'].widget.attrs['disabled'] = True

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
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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

            exam_page.excel_submit_cnt = str(int(exam_page.excel_submit_cnt)+1)
            exam_page.excel_answer = output_save_file
            _, score = excel_question.score_(output_save_file)
            exam_page.excel_result = round(exam_page.exam.excel_score * score, 1)
            exam_page.save()
            
            uploadsucc = True
    else:
        form = UploadExcelForm()

    if not exam_page.enabled:
        form.fields['file'].widget.attrs['disabled'] = True

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
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        return HttpResponseRedirect(reverse('exam:login'))

    uploadsucc = False
    ppt_question = exam_page.ppt_questions_pk_()
    if request.method == 'POST':
        form = UploadPPTForm(request.POST, request.FILES)
        if form.is_valid():
            output_save_path = exam_page.ppt_answer_save_path_()
            if os.path.exists(output_save_path): shutil.rmtree(output_save_path)
            os.makedirs(output_save_path)

            output_save_file = os.path.join(output_save_path, 'ppt.pptx')
            handle_uploaded_file(request.FILES['file'], output_save_file)

            exam_page.ppt_submit_cnt = str(int(exam_page.ppt_submit_cnt)+1)
            exam_page.ppt_answer = output_save_file
            _, score = ppt_question.score_(output_save_file)
            exam_page.ppt_result = round(exam_page.exam.ppt_score * score, 1)
            exam_page.save()
            
            uploadsucc = True
    else:
        form = UploadPPTForm()
    if not exam_page.enabled:
        form.fields['file'].widget.attrs['disabled'] = True

    context = {
        'exam': exam_page.exam,
        'student': exam_page.student,
        'exam_page': exam_page,
        'ppt_question': ppt_question,
        'form': form,
        'uploadsucc': uploadsucc,
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
    
    exam_papers = exam.exampaper_set.order_by('student_id_local')
    # for exam_paper in exam_papers:
        # print(exam_paper.student, exam_paper.student.id)
    context = {
        'exam': exam,
        'exam_id': exam_id,
        'exam_papers': exam_papers,
        'login_url': 'http://'+get_host_ip()+':8000/exam',
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
            unique_key = str(exam_id)+'-'+str(student_id)

            exam = Exam.objects.get(pk=exam_id)
            student = Student.objects.get(student_id=student_id)

            # 检查该考场和学号对应的试卷是否存在，不存在就创建新的试卷
            # 同时随机抽取题目
            choice_question_numb = exam.choice_question_num
            exam_paper, created = ExamPaper.objects.get_or_create(student=student, exam=exam, unique_key=unique_key)
            if created or exam_paper.is_empty_():
                exam_paper.problem_type = exam.problem_type
                exam_paper.start_time = timezone.now()
                if exam_paper.problem_type == '1':
                    exam_paper.end_time = timezone.now() + datetime.timedelta(hours=1, minutes=30)
                if exam_paper.problem_type == '2':
                    exam_paper.end_time = timezone.now() + datetime.timedelta(hours=2, minutes=0)
                exam_paper.student_id_local = student_id
                exam_paper.exam_id_local = exam_id

                #########
                if exam.choice_question_num and exam.choice_question_score:
                    choice_questions_ids = [str(x['id']) for x in ChoiceQuestion.objects.values('id')]
                    choice_questions_ids = random.sample(choice_questions_ids, choice_question_numb)
                    exam_paper.choice_questions = ','.join(choice_questions_ids)
                    exam_paper.choice_question_answers = ','.join(['+' for i in range(len(choice_questions_ids))])
                    exam_paper.choice_question_results = ','.join(['0' for i in range(len(choice_questions_ids))])

                #########
                if exam.text_score:
                    questions_ids = [str(x['id']) for x in TextQuestion.objects.values('id')]
                    exam_paper.text_question =  random.sample(questions_ids, 1)[0]

                if exam.file_operation_score:
                    system_questions_ids = [str(x['id']) for x in FileOperationQuestion.objects.values('id')]
                    exam_paper.system_operation_question =  random.sample(system_questions_ids, 1)[0]

                if exam.email_score:
                    email_questions_ids = [str(x['id']) for x in EmailQuestion.objects.values('id')]
                    exam_paper.email_question =  random.sample(email_questions_ids, 1)[0]
                    
                if exam.word_score:
                    questions_ids = [str(x['id']) for x in WordQuestion.objects.values('id')]
                    exam_paper.word_question =  random.sample(questions_ids, 1)[0]
                    
                if exam.excel_score:
                    questions_ids = [str(x['id']) for x in ExcelQuestion.objects.values('id')]
                    exam_paper.excel_question =  random.sample(questions_ids, 1)[0]
                    
                if exam.ppt_score:
                    questions_ids = [str(x['id']) for x in PPTQuestion.objects.values('id')]
                    exam_paper.ppt_question =  random.sample(questions_ids, 1)[0]
                
                exam_paper.save()

            return HttpResponseRedirect(reverse('exam:exampage', args=(exam_paper.unique_key,)))
    else:
        form = StudentForm()

    context = {
        'form': form,
        }
    return render(request, 'polls/login.html', context)



@csrf_exempt
def api_download_scorelist_txt(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        raise Http404("exam does not exist")

    exam_papers = exam.exampaper_set.order_by('student_id_local')
    line_head ="编号 班级 姓名 学号 选择题 文件操作题 上网题 Word题 Excel题 PPT题 总分"
    lines = [line_head]
    for i,exam_paper in enumerate(exam_papers):
        one_line = ' '.join([str(i), exam_paper.student.class_name, exam_paper.student.student_name, 
        exam_paper.student.student_id,
        exam_paper.choice_question_results,
        exam_paper.system_operation_result,
        exam_paper.email_result,
        exam_paper.word_result,
        exam_paper.excel_result,
        exam_paper.ppt_result,
        str(exam_paper.total_score())])
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


from openpyxl import Workbook

@csrf_exempt
def api_download_scorelist_xlsx(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        raise Http404("exam does not exist")

    wb = Workbook()
    ws = wb.active

    exam_papers = exam.exampaper_set.order_by('student_id_local')
    line_head ="编号 班级 姓名 学号 选择题 文字录入题 上网题 文件操作题 Word题 Excel题 PPT题 总分"
    ws.append(line_head.split(' '))
    for i,exam_paper in enumerate(exam_papers):
        one_line = [str(i), exam_paper.student.class_name, exam_paper.student.student_name, 
        exam_paper.student.student_id,
        exam_paper.choice_question_results,
        float(exam_paper.text_question_result),
        float(exam_paper.email_result),
        float(exam_paper.system_operation_result),
        float(exam_paper.word_result),
        float(exam_paper.excel_result),
        float(exam_paper.ppt_result),
        exam_paper.total_score()]
        ws.append(one_line)
    
    file_path = 'media/temp_scorelist/scorelist{}.xlsx'.format(exam_id)
    wb.save(file_path)

    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="scorelist{}.xlsx"'.format(exam_id)
    return response


@csrf_exempt
def api_get_server_time(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')

    # start_time = exam_page.start_time.replace(tzinfo=None)
    diff = int(timezone.now().timestamp() - exam_page.start_time.timestamp())
    if not exam_page.enabled:
        diff = 0
    elif exam_page.problem_type == '1':
        diff = (90+exam_page.add_time)*60 - diff
    elif exam_page.problem_type == '2':
        diff = (120+exam_page.add_time)*60 - diff

    a = {}
    a["refresh"] = 0
    a["color"] = 'black'
    if diff < 60*5: 
        a["color"] = 'red'
    if diff < 0:  
        diff = 0
        if exam_page.enabled:
            exam_page.disable_()
            a["refresh"] = 1  

    a["result"] = str(int(diff/60))+'分钟'+str(diff%60)+'秒'  ##"post_success"
    return HttpResponse(json.dumps(a), content_type='application/json')


@csrf_exempt
def api_handle_choice_answer(request, exampage_id, choice_question_id, choice_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    
    system_question = exam_page.system_questions_pk_()

    file_path = system_question.zipfile_path_()
    if file_path:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="exam.zip"'
        return response
    else:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')



@csrf_exempt
def api_download_word_zipfile(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
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


@csrf_exempt
def api_submit_all(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    
    if exam_page.enabled:
        exam_page.disable_()
    a = {"result":"null"}
    return HttpResponse(json.dumps(a), content_type='application/json')


@csrf_exempt
def add_time_enable(request, exampage_id):

    try:
        exam_page = ExamPaper.objects.get(unique_key=exampage_id)
    except ExamPaper.DoesNotExist:
        a = {"result":"null"}
        return HttpResponse(json.dumps(a), content_type='application/json')
    
    exam_page.add_time_enable_(3)
    a = {"result":"null"}
    return HttpResponse(json.dumps(a), content_type='application/json')