from rest_framework import serializers
from .models import Question, Answer, Review
from user.serializers import UserProfileSerializer, UserProfileMiniSerializer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'content',
            'correct'
        ]


class QuestionMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'title',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileMiniSerializer(many=False)
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
    author = UserProfileMiniSerializer(many=False)
    review = ReviewSerializer(many=True)
    solved_by = UserProfileMiniSerializer(many=True)
    get_average_review = serializers.ReadOnlyField()

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
            'get_average_review',
            'review'
        ]
        read_only_fields = ('author', 'answer')

