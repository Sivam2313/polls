from django.shortcuts import render
from django.http import HttpResponse
from .models import Choices, Question
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class Home (ListView):
    model = Question
    context_object_name = "question_list"
    template_name = "index.html"

def create(request):
    if request.user is None:
        return redirect('/login')
    context = {}
    if request.method == "POST":
        question = Question.objects.create(question=request.POST['question_name'],created_by=request.user)
        Choices.objects.create(question=question,choice_text = request.POST['choice3'],count = 0)
        Choices.objects.create(question=question,choice_text = request.POST['choice1'],count = 0)
        Choices.objects.create(question=question,choice_text = request.POST['choice2'],count = 0)    
        return redirect('/polls/home')
    return render(request,'create.html',context)


def register_user(request):
    context = {}
    if request=="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username,email=email,password=password)
        return redirect('/polls/home')
    return render(request,'register.html')

def login_user(request):
    context = {
        "error":"none",
    }
    if request=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('/polls/home')
        else:
            context = {
                "error":"Wrong Username or Password",
            }
            return render(request,"login.html",context)
    return render(request,'login.html',context)


def logout_user(request):
    logout(request)
    return redirect('/polls/home')

def view_profile(request):
    question = Question.objects.all().filter(created_by=request.user)
    context = {
        "question_list" : question
    }
    return render(request,'profile.html',context)

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