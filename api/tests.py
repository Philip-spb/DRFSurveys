from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from .models import *


class SurveyTestCase(APITestCase):

    def setUp(self):
        # Создаем нового пользвователя в нашем приложении
        user = User.objects.create(username='new_user', email='new_user@gmail.com')
        user.set_password('HelloWorld')
        user.save()

    def test_create_survey_api(self):
        # Логинимся нашим пользователем в системе
        url = reverse('api:login')
        data = {
            'username': 'new_user',
            'password': 'HelloWorld',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Получаем токен для доступа к функциям администратора (например для создания новых опросов)
        token = response.data.get('token', 0)
        token_len = len(token)
        self.assertGreater(token_len, 0)

        # Создаем новый "Тестовый опрос" при помощи API
        url = reverse('api:surveys-list')
        data = {'name': 'Тестовй опрос',}
        response = self.client.post(url, data, format='json',  HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем что новый "Тестовый опрос" создался
        qs = Survey.objects.filter(name='Тестовй опрос')
        self.assertEqual(qs.count(), 1)
