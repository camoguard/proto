from django.test import TestCase

from proto.accounts.models import User
from proto.forums.models import Forum, Thread, Post


class ForumModelsTestCase(TestCase):
    fixtures = ['accounts_testusers']

    def setUp(self):
        self.user = User.objects.get(pk=2)
        self.forum = Forum.objects.get(pk=1)

    def test_forum_last_post_caching(self):
        thread = Thread.objects.create(forum=self.forum, title='You Have To See This', creator=self.user)
        post = Post.objects.create(thread=thread, body='Look at this cool thing I found.', creator=self.user)

        # It's not cached yet, so it should hit the database
        with self.assertNumQueries(1):
            self.forum.last_post()

        # It's cached now, so it shouldn't hit the database
        with self.assertNumQueries(0):
            print self.forum.last_post()

    def test_thread_last_post_caching(self):
        thread = Thread.objects.create(forum=self.forum, title='You Should Check This Out Too', creator=self.user)
        post = Post.objects.create(thread=thread, body="It is way cooler than that other thing.", creator=self.user)

        # The post isn't cached yet, so it should hit the database
        with self.assertNumQueries(1):
            thread.last_post()

        # It's cached now, so it shouldn't hit the database
        with self.assertNumQueries(0):
            print thread.last_post()
