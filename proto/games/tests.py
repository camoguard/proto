from django.test import TestCase
from django.test.client import Client

from proto.games.models import Game


class WikiViewTestCase(TestCase):
    fixtures = ['testusers']

    def setUp(self):
        self.game = Game.objects.create(name='Mass Effect 3', slug='mass-effect-3',
                                        deck='A game that takes place in space.',
                                        wiki_content='<p>Coming soon to game consoles near you.</p>')

        self.client = Client()

    def test_detail_view(self):
        response = self.client.get('/wiki/game/mass-effect-3/')
        self.assertEqual(response.status_code, 200)

    def test_history_view(self):
        response = self.client.get('/wiki/game/mass-effect-3/history/')
        self.assertEqual(response.status_code, 200)



    def test_update_view_for_anonymous_user(self):
         # Test that an anonymous user gets redirected
        response = self.client.get('/wiki/create/game/')
        self.assertEqual(response.status_code, 302)

    def test_update_view(self):
        # Test that a user can edit the game
        self.client.login(username='test_user', password='test')
        response = self.client.get('/wiki/game/mass-effect-3/edit/')
        self.assertEqual(response.status_code, 200)



    def test_create_view_for_anonymous_user(self):
        # Test that an anonymous user gets redirected
        response = self.client.get('/wiki/create/game/')
        self.assertEqual(response.status_code, 302)

    def test_create_view_without_permission(self):
        # Test that a user without permission is forbidden to create a game
        self.client.login(username='test_user', password='test')
        response = self.client.get('/wiki/create/game/')
        self.assertEqual(response.status_code, 403)

    def test_create_view_with_permission(self):
        # Test that a user with permission can create a game
        self.client.login(username='test_superuser', password='test')
        response = self.client.get('/wiki/create/game/')
        self.assertEqual(response.status_code, 200)



    def test_delete_view(self):
        # Test that an anonymous user gets redirected
        response = self.client.get('/wiki/game/mass-effect-3/delete/')
        self.assertEqual(response.status_code, 302)

    def test_delete_view_without_permission(self):
        # Test that a user without permission is forbidden to delete the game
        self.client.login(username='test_user', password='test')
        response = self.client.get('/wiki/game/mass-effect-3/delete/')
        self.assertEqual(response.status_code, 403)

    def test_delete_view_with_permission(self):
        # Test that a user with permission can create the game
        self.client.login(username='test_superuser', password='test')
        response = self.client.get('/wiki/game/mass-effect-3/delete/')
        self.assertEqual(response.status_code, 200)
