# news/tests/test_routes.py
# Импортируем класс HTTPStatus.
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
# Импортируем функцию reverse().
from django.urls import reverse

from notes.models import Note

TEST_USER = 'testuser'
TEST_PASSWORD = 'password123'

class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаём пользователя
        cls.user = get_user_model().objects.create_user(
            username=TEST_USER,
            password=TEST_PASSWORD
        )

        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='test-slug',
            author=cls.user,
        )


    def test_pages_availability(self):
        urls = (
            ('notes:home', None),
        )

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_page_as_author(self):
        # Логинимся под созданным пользователем
        self.client.login(username=TEST_USER, password=TEST_PASSWORD)

        url = reverse('notes:detail', args=(self.note.slug,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Дополнительно можно проверить, что в контексте вернулась именно эта заметка
        self.assertEqual(response.context['note'], self.note)