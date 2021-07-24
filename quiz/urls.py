from django.urls import path, include
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'question', viewset=views.QuestionViewSet)
router.register(r'review', viewset=views.ReviewViewSet, basename='review')


urlpatterns = [
    path('', include(router.urls))
]