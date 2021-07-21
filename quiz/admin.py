from django.contrib import admin
from .models import Question, Answer


class AnswerInlineModel(admin.TabularInline):
    model = Answer
    fields = [
        'content',
        'correct'
    ]


admin.site.register(Answer)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'points',
        'solved_by',
        'author'
    ]
    list_display = [
        'title',
    ]
    inlines = [
        AnswerInlineModel
    ]
