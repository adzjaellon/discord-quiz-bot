from rest_framework import serializers
from .models import Question, Answer
from user.serializers import UserProfileSerializer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'content',
            'correct'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only=True)
    author = UserProfileSerializer(many=False)

    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'answer',
            'points',
            'author',
            'created'
        ]
        read_only_fields = ('author', 'answer')