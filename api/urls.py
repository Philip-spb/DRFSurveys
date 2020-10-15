from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import *

router = DefaultRouter()
router.register(r'surveys', SurveyViewSet)
router.register(r'active-surveys', ActiveSurveyViewSet)
router.register(r'full-surveys', FullSurveyViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('test-base/', TestBaseView.as_view()),
    path('test-base/<int:pk>/', SingleTestBaseView.as_view()),
    path('single-user-test-base/<int:user>/', SingleUserTestBaseView.as_view()),
    path('login/', views.obtain_auth_token),
]

urlpatterns += router.urls
