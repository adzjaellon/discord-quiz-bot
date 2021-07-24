from rest_framework import serializers
from .models import Question, Answer, Review
from user.serializers import UserProfileSerializer


class QuestionMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'title',
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'content',
            'correct'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(many=False)
    question = QuestionMiniSerializer(many=False)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'stars',
            'question'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only=True)
    author = UserProfileSerializer(many=False)
    review = ReviewSerializer(many=True)
    solved_by = UserProfileSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'answer',
            'points',
            'author',
            'created',
            'solved_by',
            'review'
        ]
        read_only_fields = ('author', 'answer')

