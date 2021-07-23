from .models import Question, Answer
from rest_framework import viewsets
from .serializers import QuestionSerializer
from rest_framework.response import Response
from user.models import UserProfile


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

    def create(self, request, *args, **kwargs):
        if UserProfile.objects.filter(discord_id=request.data['author_id']).exists():
            profile = UserProfile.objects.get(discord_id=request.data['author_id'])
        else:
            profile = UserProfile.objects.create(discord_id=request.data['author_id'], name=request.data['name'], score=0)

        Question.objects.create(title=request.data['title'], author=profile, points=int(request.data['points']))
        question = Question.objects.filter(author=profile, title=request.data['title'])[0]
        answers = request.POST.getlist('answers')
        correct = request.data['correct']

        for i in range(0, len(answers)):
            if i == int(correct) - 1:
                Answer.objects.create(question=question, content=answers[i], correct=True)
            else:
                Answer.objects.create(question=question, content=answers[i], correct=False)

        return Response(f'Question with id {question.id} created succesfully')

    def destroy(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id', None)
        question_id = kwargs['pk']

        if Question.objects.filter(id=question_id).exists():
            question = Question.objects.get(id=question_id)
            if int(user_id) == question.author.discord_id:
                question.delete()
                return Response(f'Question with id-{question_id} deleted')
            else:
                return Response('You have no permission')
        else:
            return Response(f'Question with id: {question_id} does not exist!')

