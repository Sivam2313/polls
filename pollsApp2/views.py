from django.shortcuts import render
from django.http import HttpResponse
from .models import Choices, Question

def home (request):


    try:
        question = Question.objects.all()
    except Question.DoesNotExist:
        question = [{
            question:"no questions yet"
        }]

    context = {"question_list" : question}

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