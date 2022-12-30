from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home),
    path('create/',views.create),
    path('vote/<pollid',views.vote),
    path('result/pollid',views.result),
]