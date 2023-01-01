from django.shortcuts import render
from django.http import HttpResponse
from .models import Choices, Question
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class Home (ListView):
    model = Question
    context_object_name = "question_list"
    template_name = "index.html"

def create(request):
    context = {}
    return render(request,'create.html',context)


class Vote  (DetailView):
    model = Question
    template_name = "vote.html"
    context_object_name = "question"

def result(request, pk):
    context = {}
    return render(request,'result.html',context)

def profile(request, pk):
    context = {}
    return HttpResponse(context)