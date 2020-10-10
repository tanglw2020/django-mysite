from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from .forms import WordOpForm, WordUploadForm

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

def scan_question(request):
    response = 'scan_question'
    return HttpResponse(response)

def add_choice_question(request):
    response = 'add_choice_question'
    return HttpResponse(response)

def add_word_question(request):
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WordUploadForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data)

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('polls:set_word_operation'))
    else:
        form = WordUploadForm()

    context = {
        'form': form,
        }
    return render(request, 'polls/add_word_question.html', context)

def add_excel_question(request):
    response = 'add_excel_question'
    return HttpResponse(response)

def add_ppt_question(request):
    response = 'add_ppt_question'
    return HttpResponse(response)

def set_word_operation(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WordOpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data)

            ## cleaned_data 可以用于重新初始化
            # form2 = WordOpForm(form.cleaned_data)
            # context = {
            # 'title': "Word操作题录入页面",
            # 'form': form2
            # }
            # return render(request, 'polls/input_word_operation.html', context)
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('polls:set_word_operation'))
    else:
        form = WordOpForm()

    context = {
        'title': "Word操作题录入页面",
        'form': form,
        }
    return render(request, 'polls/set_word_operation.html', context)
