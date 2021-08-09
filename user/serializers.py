from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    questions_number = serializers.ReadOnlyField()
    reviews_number = serializers.ReadOnlyField()
    correct_rate = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'name',
            'score',
            'discord_id',
            'questions_number',
            'reviews_number',
            'total_attempts',
            'successful_attempts',
            'correct_rate'
        ]
        read_only_fields = ('id',)


class UserProfileMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'name',
            'discord_id'
        ]
        read_only_fields = ('id',)
