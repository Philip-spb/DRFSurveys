from datetime import date
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from django.db.models import Q


# Получаем список всех опросов
class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


# Получаем список всех вопросов
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


# Получаем список всех ответов
class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


# Получаем список всех активных опросов
class ActiveSurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.filter(Q(start__lte=date.today().strftime('%Y-%m-%d')), Q(end__gte=date.today().strftime('%Y-%m-%d')))
    serializer_class = ActiveSurveySerializer


# Получаем список всех опросов с вопросами и вариантами ответов
class FullSurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = FullSurveySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


# Получаем список всех даных ответов
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


# Вывод всех тестов и создание нового
class TestBaseView(APIView):

    def get(self, request):
        test_base = TestBase.objects.all()
        serializer = TestBaseSerializer(test_base, many=True)
        return Response({"test_base": serializer.data})

    def post(self, request):
        test_base = request.data.get('test_base')

        serializer = TestBaseSerializerList(data=test_base)
        if serializer.is_valid(raise_exception=True):
            test_base_saved = serializer.save()
            survey_id = serializer.validated_data['survey_id']
            tb = TestBase.objects.get(pk=test_base_saved.id)
            sur = Survey.objects.get(pk=survey_id)
            for question in sur.questions.all():
                cho = ", ".join([choice.choice for choice in question.choices.all()])
                ans = Answer.objects.create(
                    test_base=tb,
                    question=question.text,
                    question_type=QUESTION_TYPE[question.type][1],
                    choices=cho)
                ans.save()
                del ans

        return Response({"test_base": test_base_saved.id})


# Вывод одного проводимого теста с отвеченными вопросами
class SingleTestBaseView(APIView):

    def get(self, request, pk):
        test_base = TestBase.objects.filter(pk=pk)
        serializer = SingleTestBaseSerializer(test_base, many=True)
        return Response({"test_base": serializer.data})


# Вывод всех тестов на которые отвечал конкретный пользователль
class SingleUserTestBaseView(APIView):

    def get(self, request, user):
        test_base = TestBase.objects.filter(user=user)
        serializer = SingleTestBaseSerializer(test_base, many=True)
        return Response({"single_user_tests": serializer.data})
