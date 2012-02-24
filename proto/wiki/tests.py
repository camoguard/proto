from django.test import TestCase

from proto.wiki.models import Wiki


class TestGame(Wiki):
    pass


class WikiViewsTestCase(TestCase):
    fixtures = ['accounts_testusers']

    def setUp(self):
        self.game_1 = TestGame.objects.create(name='Mass Effect 3',
                                              deck='A game that takes place in space.',
                                              wiki_content='This game must have a huge advertising budget.')

        self.game_2 = TestGame.objects.create(name='Half-Life 3',
                                              deck='A game that is never coming out.',
                                              wiki_content='Sorry, Half-Life fans.')

    def test_detail_view(self):
        response = self.client.get('/wiki/testgame/mass-effect-3/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('object', response.context)
        self.assertEqual(response.context['object'], self.game_1)

    def test_list_view(self):
        response = self.client.get('/wiki/testgame/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], [repr(self.game_1), repr(self.game_2)])

    def test_history_view(self):
        response = self.client.get('/wiki/testgame/mass-effect-3/history/')
        self.assertEqual(response.status_code, 200)



    def test_update_view_for_anonymous_user(self):
         # Test that an anonymous user gets redirected
        response = self.client.get('/wiki/create/game/')
        self.assertEqual(response.status_code, 302)

    def test_update_view(self):
        # Test that a user can edit the game
        self.client.login(username='test_user', password='test')
        response = self.client.get('/wiki/testgame/mass-effect-3/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('object', response.context)
        self.assertEqual(response.context['object'], self.game_1)

    def test_update_view_with_good_data(self):
        # Test that we can successfully edit a game with good data
        self.client.login(username='test_superuser', password='test')
        response = self.client.post('/wiki/testgame/mass-effect-3/edit/', {
                                    'deck': 'This game is a space soap opera.',
                                    'wiki_content': 'This game must have a huge advertising budget.'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/wiki/testgame/mass-effect-3/')
        self.assertEqual(TestGame.objects.all().count(), 2)

    def test_update_view_with_bad_data(self):
        # Test that an attempt to edit a game with bad data fails
        self.client.login(username='test_superuser', password='test')

        # Send empty post data
        response = self.client.post('/wiki/testgame/mass-effect-3/edit/', {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].is_valid(), False)

        # Send bad post data
        response = self.client.post('/wiki/testgame/mass-effect-3/edit/', {
                                    'wiki_content': 'Is this one in Africa too?'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'deck', 'This field is required.')



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
        self.assertIn('form', response.context)
        self.assertIn('model', response.context)

    def test_create_view_with_good_data(self):
        # Test that we can successfully create a game with good data
        self.client.login(username='test_superuser', password='test')
        response = self.client.post('/wiki/create/testgame/', {
                                    'name': 'Far Cry 3',
                                    'deck': 'A game where you shoot things.',
                                    'wiki_content': 'Is this one in Africa too?'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/wiki/testgame/far-cry-3/')
        self.assertEqual(TestGame.objects.all().count(), 3)

    def test_create_view_with_bad_data(self):
        # Test that an attempt to create a game with bad data fails
        self.client.login(username='test_superuser', password='test')

        # Send empty post data
        response = self.client.post('/wiki/create/testgame/', {})
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].is_valid(), False)

        # Send bad post data
        response = self.client.post('/wiki/create/testgame/', {
                                    'deck': 'A game where you shoot things.',
                                    'wiki_content': 'Is this one in Africa too?'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')



    def test_delete_view(self):
        # Test that an anonymous user gets redirected
        response = self.client.get('/wiki/testgame/mass-effect-3/delete/')
        self.assertEqual(response.status_code, 302)

    def test_delete_view_without_permission(self):
        # Test that a user without permission is forbidden to delete the game
        self.client.login(username='test_user', password='test')
        response = self.client.get('/wiki/testgame/mass-effect-3/delete/')
        self.assertEqual(response.status_code, 403)

    def test_delete_view_with_permission(self):
        # Test that a user with permission can create the game
        self.client.login(username='test_superuser', password='test')
        response = self.client.get('/wiki/testgame/mass-effect-3/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.game_1)
