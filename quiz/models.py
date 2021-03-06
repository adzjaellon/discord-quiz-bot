from django.db import models
from user.models import UserProfile
from django.db.models import Avg


class Question(models.Model):
    title = models.CharField(max_length=222)
    points = models.SmallIntegerField()
    created = models.DateField(auto_now_add=True)
    solved_by = models.ManyToManyField(UserProfile, related_name='questions_done', blank=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='question')

    @property
    def get_average_review(self):
        return self.review.aggregate(average=Avg('stars'))

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


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='review')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='review')
    stars = models.FloatField()

    def __str__(self):
        return f'{self.user} {self.question} {self.stars}'

    class Meta:
        ordering = ('-stars',)
