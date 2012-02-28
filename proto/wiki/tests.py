from django import forms
from django.test import TestCase

from proto.wiki.models import Wiki


class TestGame(Wiki):
    pass


class WikiViewsTestCase(TestCase):
    fixtures = ['accounts_testusers']

    def setUp(self):
        self.game = TestGame.objects.create(name='Mass Effect 3',
                                            deck='A game that takes place in space.',
                                            wiki_content='This game must have a huge advertising budget.')

    def test_detail_view(self):
        response = self.client.get('/wiki/%s/%s/' % (self.game._class, self.game.slug))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.game)

    def test_list_view(self):
        TestGame.objects.create(name='Half-Life 3',
                                deck='A game that is never coming out.',
                                wiki_content='Sorry, Half-Life fans.')
        response = self.client.get('/wiki/testgame/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'],
                                ['<TestGame: Half-Life 3>', '<TestGame: Mass Effect 3>'])

    def test_history_view(self):
        response = self.client.get('/wiki/%s/%s/history/' % (self.game._class, self.game.slug))
        self.assertEqual(response.status_code, 200)



    def test_update_view_for_anonymous_user(self):
         # Test that an anonymous user gets redirected to login page
        response = self.client.get('/wiki/%s/%s/edit/' % (self.game._class, self.game.slug))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'http://testserver/accounts/login/?next=/wiki/%s/%s/edit/' %
                            (self.game._class, self.game.slug))

    def test_update_view(self):
        self.client.login(username='test_user', password='test')
        response = self.client.get('/wiki/%s/%s/edit/' % (self.game._class, self.game.slug))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], forms.ModelForm)
        # Test that the 'name' field has been removed from the form since we don't allow users
        # to edit the names of wiki pages
        self.assertNotIn('name', response.context['form'].fields)
        self.assertEqual(response.context['object'], self.game)

    def test_update_view_post_with_good_data(self):
        self.client.login(username='test_superuser', password='test')
        response = self.client.post('/wiki/%s/%s/edit/' % (self.game._class, self.game.slug), {
                                    'deck': 'This game is a space soap opera.',
                                    'wiki_content': 'This game must have a huge advertising budget.'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'http://testserver/wiki/%s/%s/' % (self.game._class, self.game.slug))
        self.assertQuerysetEqual(TestGame.objects.all(), ['<TestGame: Mass Effect 3>'])

    def test_update_view_post_with_bad_data(self):
        self.client.login(username='test_superuser', password='test')

        # Send empty post data
        response = self.client.post('/wiki/%s/%s/edit/' % (self.game._class, self.game.slug), {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].is_valid(), False)

        # Send bad post data
        response = self.client.post('/wiki/%s/%s/edit/' % (self.game._class, self.game.slug), {
                                    'wiki_content': 'Is this one in Africa too?'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'deck', 'This field is required.')



    def test_create_view_for_anonymous_user(self):
        # Test that an anonymous user gets redirected to login page
        response = self.client.get('/wiki/create/testgame/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'http://testserver/accounts/login/?next=/wiki/create/testgame/')

    def test_create_view_without_permission(self):
        # Test that a user without permission is forbidden to create a game
        self.client.login(username='test_user', password='test')
        response = self.client.get('/wiki/create/testgame/')
        self.assertEqual(response.status_code, 403)

    def test_create_view_with_permission(self):
        self.client.login(username='test_superuser', password='test')
        response = self.client.get('/wiki/create/testgame/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('object', response.context)
        self.assertIsInstance(response.context['form'], forms.ModelForm)
        # Test that the form contains the 'name' field since we're creating an object
        self.assertIn('name', response.context['form'].fields)
        self.assertIn('model', response.context)

    def test_create_view_post_with_good_data(self):
        self.client.login(username='test_superuser', password='test')
        response = self.client.post('/wiki/create/testgame/', {
                                    'name': 'Far Cry 3',
                                    'deck': 'A game where you shoot things.',
                                    'wiki_content': 'Is this one in Africa too?'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'http://testserver/wiki/testgame/far-cry-3/')
        self.assertQuerysetEqual(TestGame.objects.all(), ['<TestGame: Far Cry 3>', '<TestGame: Mass Effect 3>'])

    def test_create_view_post_with_bad_data(self):
        self.client.login(username='test_superuser', password='test')

        # Send empty post data
        response = self.client.post('/wiki/create/testgame/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].is_valid(), False)

        # Send bad post data
        response = self.client.post('/wiki/create/testgame/', {
                                    'deck': 'A game where you shoot things.',
                                    'wiki_content': 'Is this one in Africa too?'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')



    def test_delete_view_for_anonymous_user(self):
        # Test that an anonymous user gets redirected to login page
        response = self.client.get('/wiki/%s/%s/delete/' % (self.game._class, self.game.slug))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'http://testserver/accounts/login/?next=/wiki/%s/%s/delete/' %
                            (self.game._class, self.game.slug))

    def test_delete_view_without_permission(self):
        # Test that a user without permission is forbidden to delete the game
        self.client.login(username='test_user', password='test')
        response = self.client.get('/wiki/%s/%s/delete/' % (self.game._class, self.game.slug))
        self.assertEqual(response.status_code, 403)

    def test_delete_view_with_permission(self):
        self.client.login(username='test_superuser', password='test')
        response = self.client.get('/wiki/%s/%s/delete/' % (self.game._class, self.game.slug))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.game)

    def test_delete_view_post(self):
        self.client.login(username='test_superuser', password='test')
        response = self.client.post('/wiki/%s/%s/delete/' % (self.game._class, self.game.slug))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'http://testserver/wiki/testgame/')
        self.assertNotIn(self.game, TestGame.objects.all())
