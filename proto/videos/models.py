from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models

from filebrowser.fields import FileBrowseField

class Video(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    )
    title = models.CharField(max_length=100)
    deck = models.CharField(max_length=200)
    video = FileBrowseField('Video', max_length=200, directory="videos/", extensions=[".mp4"], blank=True, null=True)
    image = models.ImageField()
    pub_date = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    premium = models.BooleanField(default=False)
    comments = generic.GenericRelation(Comment, object_id_field='object_pk')
    sites = models.ManyToManyField(Site)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    on_site = CurrentSiteManager()

    def __unicode__(self):
        return self.title
