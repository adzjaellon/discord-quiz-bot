from django.db import models
from django.db.models import Count


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    discord_id = models.IntegerField()
    total_attempts = models.IntegerField(default=0)
    successful_attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-score', )

    @property
    def questions_number(self):
        return self.question.all().count()

    @property
    def reviews_number(self):
        return self.review.all().count()

    @property
    def correct_rate(self):
        if self.total_attempts == 0:
            return 0
        return round((self.successful_attempts / self.total_attempts) * 100, 2)
