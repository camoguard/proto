from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models

from proto.comments.models import ThreadedComment
from proto.common.fields import AutoSlugField
from proto.wiki.models import Wiki


class PublicManager(models.Manager):
    def get_query_set(self):
        return super(PublicManager, self).get_query_set().filter(status='p', pub_date__lte=datetime.now())


class Article(models.Model):
    " Stores a single news article. "
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    )

    title = models.CharField(max_length=70)
    author = models.ForeignKey(User, limit_choices_to = {'is_staff': True})
    deck = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title')
    body = models.TextField()
    image = models.ImageField(upload_to='images/news', null=True, blank=True)
    pub_date = models.DateTimeField('Publish date')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    tags = models.ManyToManyField(Wiki, null=True, blank=True)
    comments = generic.GenericRelation(ThreadedComment, object_id_field='object_pk')
    site = models.ForeignKey(Site)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()
    public = PublicManager()

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('article-detail', (), {
            'year': self.pub_date.year,
            'month': self.pub_date.strftime('%b'),
            'day': self.pub_date.strftime('%d'),
            'slug': self.slug})
