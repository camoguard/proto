from django.test import TestCase
from django.test.client import Client

from proto.wiki.models import WikiPage


class TestGame(WikiPage):
    pass


class WikiViewTestCase(TestCase):
    fixtures = ['testusers']

    def setUp(self):
        self.game = TestGame.objects.create(name='Mass Effect 3', slug='mass-effect-3',
                                            deck='A game that takes place in space.',
                                            wiki_content='<p>Coming soon to game consoles near you.</p>')

        self.client = Client()

    def test_detail_view(self):
        response = self.client.get('/wiki/testgame/mass-effect-3/')
        self.assertEqual(response.status_code, 200)

    def test_history_view(self):
        response = self.client.get('/wiki/testgame/mass-effect-3/history/')
        self.assertEqual(response.status_code, 200)
