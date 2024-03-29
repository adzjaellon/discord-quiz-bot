from .models import Question, Answer, Review
from rest_framework import viewsets
from rest_framework import filters
from .serializers import QuestionSerializer, ReviewSerializer
from rest_framework.response import Response
from user.models import UserProfile
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    permission_classes = [AllowAny]
    search_fields = ('title',)

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
        profile, created = UserProfile.objects.get_or_create(name=request.data['name'],
                                                             discord_id=request.data['author_id'])
        question = Question.objects.create(title=request.data['title'], author=profile,
                                           points=int(request.data['points']))
        answers = request.POST.getlist('answers')
        correct = request.data['correct']

        for i in range(0, len(answers)):
            if i == int(correct) - 1:
                Answer.objects.create(question=question, content=answers[i], correct=True)
            else:
                Answer.objects.create(question=question, content=answers[i], correct=False)

        return Response(f'Question with id {question.id} created succesfully')

    def update(self, request, *args, **kwargs):
        question = self.get_object()
        user_id = int(request.data['user_id'])
        username = request.data['username']
        rating = int(request.data['rating'])

        if rating in list(range(1, 6)):
            if UserProfile.objects.filter(discord_id=user_id).exists():
                user = UserProfile.objects.get(discord_id=user_id)
            else:
                UserProfile.objects.create(name=username, discord_id=user_id)
                user = UserProfile.objects.get(discord_id=user_id)

            print(question.review.filter(user=user).exists())
            if question.review.filter(user=user).exists():
                return Response('You already rated this question!')
            else:
                review = Review.objects.create(user=user, question=question, stars=rating)
                question.review.add(review)
                question.save()
                return Response(f'Your rate to question with id {question.id} has been saved!')
        else:
            return Response(f'Wrong rating number, allowed numbers from 1 to 5')

    def destroy(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id', None)
        question_id = kwargs['pk']

        if Question.objects.filter(id=question_id).exists():
            question = Question.objects.get(id=question_id)
            if int(user_id) == question.author.discord_id:
                question.delete()
                return Response(f'Question with id-{question_id} deleted')
            else:
                return Response('You have no permission to delete this question')
        else:
            return Response(f'Question with id: {question_id} does not exist!')

    @action(detail=False, methods=['get'])
    def get_question(self, request, **kwargs):
        id = request.query_params.get('id', None)

        if Question.objects.filter(id=id).exists():
            question = Question.objects.get(id=id)
            serializer = QuestionSerializer(question, many=False)
            return Response(serializer.data)
        else:
            return Response(f'You have no question with id: {id}')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    filter_backends = (filters.OrderingFilter, )

    def get_queryset(self):
        id = self.request.query_params.get('id', None)

        if id is not None:
            queryset = Review.objects.filter(user__discord_id=int(id))
        else:
            queryset = Review.objects.all()
        return queryset

    def destroy(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id', None)
        review_id = kwargs['pk']

        if Review.objects.filter(id=review_id).exists():
            review = Review.objects.get(id=review_id)
            if int(user_id) == review.user.discord_id:
                review.delete()
                return Response(f'Review with id: {review_id} deleted')
            else:
                return Response('You have no permission to delete this review')
        else:
            return Response(f'Your review with id {review_id} does not exist!')

