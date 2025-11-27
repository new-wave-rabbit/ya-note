# news/tests/test_content.py
from django.conf import settings
from django.test import TestCase

from notes.models import Note


class TestHomePage(TestCase):

    @classmethod
    def setUpTestData(cls):
        all_news = []
        for index in range(settings.NOTES_COUNT_ON_PAGE + 1):
            news = Note(title=f'Заметка {index}', text='Просто текст.')
            all_news.append(news)
        Note.objects.bulk_create(all_news)

