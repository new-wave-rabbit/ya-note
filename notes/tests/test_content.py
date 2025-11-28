# news/tests/test_content.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()
from notes.forms import NoteForm


class TestHomePage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Создатель')
        all_notes = []
        for index in range(settings.NOTES_COUNT_ON_PAGE + 1):
            notes = Note(
                title=f'Заметка {index}',
                text='Просто текст.',
                slug='test-slug-' + str(index),
                author=cls.author,
            )
            all_notes.append(notes)
        cls.notes = Note.objects.bulk_create(all_notes)

    def test_authorized_client_has_form(self):
        self.client.force_login(self.author)

        urls = (
            ('notes:add', None),
            ('notes:edit', (self.notes[0].slug,)),
        )

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
