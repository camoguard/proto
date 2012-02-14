from datetime import datetime

from django.contrib.contenttypes import generic
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models

from proto.comments.models import ThreadedComment
from proto.wiki.models import WikiPage


class PublicManager(models.Manager):
    def get_query_set(self):
        return super(PublicManager, self).get_query_set().filter(status='p', pub_date__lte=datetime.now())


class Video(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    )

    title = models.CharField(max_length=70)
    deck = models.CharField(max_length=100)
    category = models.ForeignKey('VideoCategory')
    file = models.FileField(upload_to='videos')
    image = models.ImageField(upload_to='images/videos')
    pub_date = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    premium = models.BooleanField(default=False)
    tags = models.ManyToManyField(WikiPage, null=True, blank=True)
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


class VideoCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'video categories'

    def __unicode__(self):
        return self.name
