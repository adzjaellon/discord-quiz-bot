from .models import Question, Answer
from rest_framework import viewsets
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        discord_id = self.request.query_params.get('discord_id', None)

        if user_id is not None:
            queryset = Question.objects.filter(author__discord_id=user_id)
        elif discord_id is not None:
            queryset = Question.objects.exclude(solved_by__discord_id__icontains=discord_id)
        else:
            queryset = Question.objects.all()
        return queryset
