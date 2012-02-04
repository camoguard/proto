from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models

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
    comments = generic.GenericRelation(Comment, object_id_field='object_pk')
    site = models.ForeignKey(Site)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return self.title


class VideoCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'video categories'

    def __unicode__(self):
        return self.name
