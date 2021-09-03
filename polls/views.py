from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.http import Http404


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
