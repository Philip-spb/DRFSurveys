from datetime import datetime

from django.db import models
from django.db.models import Q

QUESTION_TYPE = (
    (0, 'Ответ текстом'),
    (1, 'Ответ с выбором одного варианта'),
    (2, 'Ответ с выбором нескольких вариантов'),
)


class Survey(models.Model):
    name = models.CharField(max_length=1024, verbose_name='Название опроса')
    description = models.CharField(max_length=2047, blank=True, verbose_name='Описание опроса')
    start = models.DateField(null=True, blank=True, verbose_name='Дата старта')
    end = models.DateField(null=True, blank=True, verbose_name='Дата окончания')

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=1024, verbose_name='Текст вопроса')
    type = models.PositiveSmallIntegerField(choices=QUESTION_TYPE, verbose_name='Тип вопроса')
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT, related_name='questions', verbose_name='Опрос')

    def __str__(self):
        return self.text


class Choice(models.Model):
    choice = models.CharField(max_length=1024, verbose_name='Вариант ответа')
    questions = models.ForeignKey(Question, null=True, blank=True, default=None, related_name='choices',
                                  limit_choices_to=Q(type=1) | Q(type=2),
                                  on_delete=models.PROTECT, verbose_name='Вопросы')

    def __str__(self):
        return self.choice


class TestBase(models.Model):
    user = models.IntegerField(null=True, blank=True, verbose_name='ID пользователя')
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT, related_name='test_bases',
                               verbose_name='Название проходимого опроса')
    time_stamp = models.DateTimeField(auto_now=True, editable=False, verbose_name='Дата создания')

    def __str__(self):
        date = datetime.fromisoformat(str(self.time_stamp))
        return str(self.pk) + '/' + date.strftime("%d%m%Y")


class Answer(models.Model):
    test_base = models.ForeignKey(TestBase, null=True, blank=True, default=None, related_name='answers',
                                  on_delete=models.PROTECT, verbose_name='Проходимый опрос')
    question = models.CharField(max_length=1024, verbose_name='Текст вопроса')
    question_type = models.CharField(max_length=127, verbose_name='Тип вопроса')
    choices = models.CharField(null=True, blank=True, default=None, max_length=2047, verbose_name='Варианты ответа')
    answer = models.CharField(null=True, blank=True, default=None, max_length=2047, verbose_name='Ответ')

    def __str__(self):
        return self.answer
