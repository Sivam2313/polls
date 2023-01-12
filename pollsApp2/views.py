from django.shortcuts import render
from django.http import HttpResponse
from .models import Choices, Question, UserInfo
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json

def home(request):
    context = {}
    auth = True
    question = Question.objects.all()
    users = User.objects.all()
    if request.user.is_anonymous:
        context = {
            "link":"../login/",
            "text":"Login",
            "question_list":question,
            "users":users
        }   
        return render(request,'index.html',context)
    else:
        context = {
            "link":"../logout/",
            "text":"Logout",
            "question_list":question,
            "users":users.exclude(id = request.user.id)
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
        info = UserInfo.objects.create(userId=user)
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
        return redirect('/polls/home')


def logout_user(request):
    logout(request)
    return redirect('/polls/home')

def view_profile(request):
    if request.user.is_anonymous:
        return redirect('/polls/login')
    question = Question.objects.all().filter(created_by=request.user)
    context = {
        "question_list" : question
    }
    return render(request,'profile.html',context)

def vote(request,pk):
    if request.user.is_anonymous:
        return redirect('/polls/login')
    info = UserInfo.objects.get(userId=request.user)
    if pk in info.has_voted:
        return redirect('/polls/result/'+str(pk))
    question = Question.objects.get(id=pk)
    context = {
        "question":question,
    }
    if request.method == "POST":
        if question in info.noti:
            info.noti.remove(question)
            info.save()
        question.votes += 1
        question.save()
        choice_idx = request.POST["choice"]
        choice = Choices.objects.get(id=choice_idx)
        choice.count += 1
        choice.save()
        return redirect('/polls/result/'+str(pk)    )
    return render(request,'vote.html',context)

def result(request, pk):
    info = UserInfo.objects.get(userId=request.user)
    if pk not in info.has_voted:
        info.has_voted.append(pk)
        info.save()
    question = Question.objects.get(id=pk)
    choices = Choices.objects.all().filter(question=question)
    choice_list = []
    total = 0
    for choice in choices:
        total = total + choice.count;
    if total==0:
        total = 1
    for choice in choices:
        x = (int)(choice.count/total * 100)
        choice_list.append(
        {
            "choice":choice,    
            "percen":x,
        })
    context = {
        "question":question,
        "choice_list":choice_list,
    }

    return render(request,'result.html',context)


def deletePoll(request, pk):
    question = Question.objects.get(id=pk)
    question.delete()
    return redirect("/polls/home")

def shareQuestion(request,pk):
    if request.user.is_anonymous:
        return HttpResponse("login")
    question = Question.objects.get(id=pk)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    reciever = body['share']
    user = User.objects.get(id = reciever)
    info = UserInfo.objects.get(userId=user)
    if question not in info.noti:
        info.noti.append(question)
    info.save()
    print(info.noti)
    return HttpResponse('home')


def shared(request):
    info = UserInfo.objects.get(userId=request.user)
    context = {
        "question_list":info.noti,
    }
    return render(request,'shared.html',context)
