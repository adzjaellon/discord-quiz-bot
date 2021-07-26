from django.db import models


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    discord_id = models.IntegerField()

    @property
    def questions_number(self):
        return self.question.all().count()

    @property
    def reviews_number(self):
        return self.review.all().count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-score', )
