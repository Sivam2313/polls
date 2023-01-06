from django.shortcuts import render
from django.http import HttpResponse
from .models import Choices, Question
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def home(request):
    context = {}
    auth = True
    question = Question.objects.all()
    if request.user.is_anonymous:
        context = {
            "link":"../login/",
            "text":"Login",
            "question_list":question,
        }   
        return render(request,'index.html',context)
    else:
        context = {
            "link":"../logout/",
            "text":"Logout",
            "question_list":question,
        }
        return render(request, 'index.html', context)

def create(request):
    if request.user.is_anonymous:
        return redirect('/polls/login')
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
    if request.method=="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username,email=email,password=password)
        print("success")
        return redirect('/polls/home')
    return render(request,'register.html')

def login_user(request):
    if request.user.is_anonymous:
        context = {
            "error":"none",
        }
        if request.method=="POST":
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
    else:
        return redirect('/index')


def logout_user(request):
    logout(request)
    return redirect('/polls/home')

def view_profile(request):
    if request.user.is_anonymous:
        return redirect('/login')
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