from django.db import models
from user.models import UserProfile


class Question(models.Model):
    title = models.CharField(max_length=222)
    points = models.SmallIntegerField()
    created = models.DateField(auto_now_add=True)
    solved_by = models.ManyToManyField(UserProfile, related_name='questions_done', blank=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='question')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    content = models.CharField(max_length=222)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question} {self.content[:15]}'
