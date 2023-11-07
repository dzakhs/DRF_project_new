from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from lms.models import Course, Lesson, Subscription
from users.models import User
from lms.serializers import LessonSerializer

class LessonTestCase(APITestCase):

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create(
            email='test@test.ru',
            password='123qwe456rty'
        )
        self.client.force_authenticate(user=self.user)

        # Создание тестового курса
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            image=None,
            owner=self.user
        )

        # Создание тестовой подписки
        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            is_subscribed=True
        )

    def test_create_lesson(self):


        url = reverse('lms:lesson-create')
        data = {
            'title': 'Тест',
            'description': 'Тест',
            'url': 'https://www.youtube.com/',
            'course': self.course.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().title,
                         'Тест')

    def test_update_lesson(self):


        lesson = Lesson.objects.create(
            title='Test',
            description='Test',
            url='https://www.youtube.com/',
            course=self.course,
            owner=self.user
        )

        url = reverse('lms:lesson-update', kwargs={'pk': lesson.pk})
        data = {
            'title': 'Тест',
            'description': 'Тест',
            'url': 'https://www.youtube.com/',
            'course': self.course.pk
        }

        response = self.client.put(url, data=data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['title'], data['title'])
        self.assertEquals(response.data['description'], data['description'])
        self.assertEquals(response.data['url'], data['url'])
        self.assertEquals(response.data['course'], data['course'])

    def test_delete_lesson(self):

        lesson = Lesson.objects.create(title='Тест',
                                   description='Тест',
                                   url='https://www.youtube.com/',
                                   image=None,
                                   course=self.course,
                                   owner=self.user
                                   )
        url = reverse('lms:lesson-delete', kwargs={'pk': lesson.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())



class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@test.ru',
            password='123qwe456rty'
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title='Тестовый курс')

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            is_subscribed=True
        )

    def test_subscription_create(self):
        url = reverse('lms:subscribe-create')
        data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'is_subscribed': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_delete(self):
        url = reverse('lms:subscribe-delete', kwargs={'pk': self.subscription.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)