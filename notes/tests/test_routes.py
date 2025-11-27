# news/tests/test_routes.py
# Импортируем класс HTTPStatus.
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
# Импортируем функцию reverse().
from django.urls import reverse

from notes.models import Note

User = get_user_model()
TEST_USER_1 = 'testuser_1'
TEST_USER_2 = 'testuser_2'
TEST_PASSWORD = 'password123'

class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаём пользователя
        
        cls.user_1 = User.objects.create(username=TEST_USER_1)
        cls.user_2 = User.objects.create(username=TEST_USER_2)

        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='test-slug',
            author=cls.user_1,
        )

    # Не авторизованный пользователь должен получать статус 200
    def test_pages_availability(self):
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:signup', None),
        )

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    # Автор должен иметь доступ к редактированию и удалению своей заметки
    def test_availability_for_note_view_edit_and_delete(self):
        users_statuses = (
            (self.user_1, HTTPStatus.OK),
            (self.user_2, HTTPStatus.NOT_FOUND),
        )
        urls = (
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )

        for user, status in users_statuses:
            self.client.force_login(user)
            for name, args in urls:
                with self.subTest(name=name):
                    url = reverse(name, args=args)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    # Авторизоанный пользователь должен получать статус 200
    def test_pages_availability_for_authorized(self):
        urls = (
            ('notes:add', None),
            ('notes:list', None),
            ('notes:success', None),
        )
        self.client.force_login(self.user_1)

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
