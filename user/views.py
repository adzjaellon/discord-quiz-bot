from .models import UserProfile
from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from quiz.models import Question
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = (filters.OrderingFilter,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        count = self.request.query_params.get('param', None)
        id = self.request.query_params.get('id', None)

        if count is not None:
            if count.isdigit():
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

    @action(detail=False, methods=['get'])
    def profile_details(self, request, **kwargs):
        id = self.request.query_params.get('id', None)
        if UserProfile.objects.filter(discord_id=id).exists():
            user = UserProfile.objects.get(discord_id=id)
            serializer = UserProfileSerializer(user, many=False)
            return Response(serializer.data)
        else:
            return Response('Your profile does not exist! Solve some questions to be listed on ranking')

    @action(detail=False, methods=['get', 'put'])
    def increase_attempts(self, request, **kwargs):
        id = self.request.query_params.get('id', None)
        name = self.request.query_params.get('name', None)

        if UserProfile.objects.filter(discord_id=id).exists():
            user = UserProfile.objects.get(discord_id=id)
            user.total_attempts += 1
            user.save()
            serializer = UserProfileSerializer(user, many=False)
        else:
            UserProfile.objects.create(name=name, discord_id=id, total_attempts=1)
            user = UserProfile.objects.get(discord_id=id)
            serializer = UserProfileSerializer(user, many=False)

        return Response(serializer.data)

    @action(detail=False, methods=['get', 'put'])
    def increase_successful_attempts(self, request, **kwargs):
        id = self.request.query_params.get('id', None)
        user = UserProfile.objects.get(discord_id=id)
        user.successful_attempts += 1
        user.save()
        serializer = UserProfileSerializer(user, many=False)

        return Response(serializer.data)
