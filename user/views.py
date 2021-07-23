from .models import UserProfile
from rest_framework import viewsets
from rest_framework import status
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from quiz.models import Question


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        count = self.request.query_params.get('param', None)
        id = self.request.query_params.get('id', None)

        if count is not None:
            if count < 1:
                return None
            elif count.isdigit():
                queryset = UserProfile.objects.all()[:int(count)]
            else:
                queryset = UserProfile.objects.filter(discord_id=id)
        elif id is not None:
            queryset = UserProfile.objects.filter(discord_id=id)
        else:
            queryset = UserProfile.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        print('request data create/update user profile', request.data)
        serializer = UserProfileSerializer(data=request.data)
        question_id = request.data['question_id']
        if serializer.is_valid():
            name = serializer.validated_data['name']
            points = serializer.validated_data['score']
            discord_id = serializer.validated_data['discord_id']
            question = Question.objects.get(id=question_id)

            if UserProfile.objects.filter(discord_id=discord_id).exists():
                user = UserProfile.objects.get(discord_id=discord_id)
                serializer = UserProfile.objects.get(discord_id=discord_id)
                serializer.score += int(points)
                question.solved_by.add(user)

            serializer.save()

            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)