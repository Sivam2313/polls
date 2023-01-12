from django.contrib import admin

from .models import Question, Choices, UserInfo


class ChoiceInline(admin.TabularInline):
    model = Choices


class QuestionAdmin(admin.ModelAdmin):
    inlines=[ChoiceInline]



admin.site.register(Question,QuestionAdmin)
admin.site.register(UserInfo)   