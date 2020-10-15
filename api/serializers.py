from rest_framework import serializers

from .models import *


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice', 'questions')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(read_only=True, many=True)
    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'survey', 'choices')


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'name', 'description', 'start', 'end')
        read_only_fields = ('start',)


class FullQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'choices')


class FullSurveySerializer(serializers.ModelSerializer):
    questions = FullQuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Survey
        fields = ('id', 'name', 'description', 'start', 'end', 'questions')


class ActiveSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'name', 'description')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'question_type', 'choices', 'answer')
        read_only_fields = ('id', 'question', 'question_type', 'choices')


class TestBaseSerializerList(serializers.ModelSerializer):
    survey = FullSurveySerializer(read_only=True)
    survey_id = serializers.IntegerField(write_only=True, label='ID опроса')

    class Meta:
        model = TestBase
        fields = ('id', 'user', 'survey', 'survey_id')


class TestBaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.CharField(max_length=120)
    survey = FullSurveySerializer(read_only=True)

    def create(self, validated_data):
        return TestBase.objects.create(**validated_data)


class SingleTestBaseSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    # user = serializers.CharField(max_length=120)
    # survey = FullSurveySerializer(read_only=True)
    answers = AnswerSerializer(read_only=True, many=True)
