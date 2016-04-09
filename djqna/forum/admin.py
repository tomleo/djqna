from django.contrib import admin

from .models import Vote, Question, Answer


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
