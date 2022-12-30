from django.shortcuts import render
from django.http import HttpResponse
from .models import Choices, Question

def home (request):


    try:
        question = Question.objects.get()[:]
    except Question.DoesNotExist:
        question = None

    context = {"question_list" : question}
    print(question)

    return render(request, 'index.html',context)

def create(request):
    context = {}
    return render(request,'create.html',context)


def vote(request, pollid):
    context = {}
    return render(request, 'vote.html', context)

def result(request, pollid):
    context = {}
    return render(request,'result.html',context)