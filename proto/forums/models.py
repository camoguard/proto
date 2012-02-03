from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import models

# CACHE KEYS
FORUM_LAST_POST_KEY = 'forums:forum:last_post:%i'
THREAD_LAST_POST_KEY = 'forums:thread:last_post:%i'

class Forum(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField()
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # content_object = generic.GenericForeignKey('content_type', 'object_id')
    site = models.ForeignKey(Site)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        unique_together = (('site', 'slug'),)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/forums/%s/" % self.slug

    def last_post(self):
        # Cache the last post so that we don't have to perform a database query for each forum on the forum list
        last_post = cache.get(FORUM_LAST_POST_KEY % self.pk)

        if last_post is None:
            try:
                last_post = Post.objects.filter(thread__forum=self).select_related('thread', 'creator', 'thread__forum').latest()
            except Post.DoesNotExist:
                last_post = None
            cache.set(FORUM_LAST_POST_KEY % self.pk, last_post, 60 * 60 * 24)  # 24 hours

        return last_post


class Thread(models.Model):
    forum = models.ForeignKey(Forum)
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/forums/%s/%i/" % (self.forum.slug, self.id)

    def last_post(self):
        # Cache the last post so that we don't have to perform a database query for each thread on the thread list
        last_post = cache.get(THREAD_LAST_POST_KEY % self.pk)
        if last_post is None:
            last_post = self.post_set.select_related('creator').latest()
            cache.set(THREAD_LAST_POST_KEY % self.pk, last_post, 60 * 60 * 24)  # 24 hours
        return last_post


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    creator = models.ForeignKey(User)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created'

    def __unicode__(self):
        return "%s by %s" % (self.created, self.creator)
