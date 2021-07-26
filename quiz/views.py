from .models import Question, Answer, Review
from rest_framework import viewsets
from rest_framework import filters
from .serializers import QuestionSerializer, ReviewSerializer
from rest_framework.response import Response
from user.models import UserProfile


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering = ('author',)
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

    def update(self, request, *args, **kwargs):
        question = self.get_object()
        user_id = int(request.data['user_id'])
        username = request.data['username']
        rating = int(request.data['rating'])

        if rating in list(range(1, 6)):
            if UserProfile.objects.filter(discord_id=user_id).exists():
                user = UserProfile.objects.get(discord_id=user_id)
            else:
                UserProfile.objects.create(name=username, discord_id=user_id, score=0)
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
                return Response('You have no permission')
        else:
            return Response(f'Question with id: {question_id} does not exist!')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering = ('-stars', )

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        print('review id', id)
        if id is not None:
            queryset = Review.objects.filter(user__discord_id=int(id))
        else:
            queryset = Review.objects.all()
        return queryset

    def destroy(self, request, *args, **kwargs):
        print('request user', request.user)
        user_id = self.request.query_params.get('user_id', None)
        review_id = kwargs['pk']

        if Review.objects.filter(id=review_id).exists():
            review = Review.objects.get(id=review_id)
            if int(user_id) == review.user.discord_id:
                review.delete()
                return Response(f'Review with id: {review_id} deleted')
            else:
                return Response('You have no permission to do that')
        else:
            return Response(f'Your review with id {review_id} does not exist!')

