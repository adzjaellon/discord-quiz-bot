from .models import Question, Answer
from rest_framework import viewsets
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
