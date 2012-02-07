from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models


class Podcast(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/podcasts')
    primary = models.BooleanField(default=False)
    site = models.ForeignKey(Site)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        unique_together = ('primary', 'site')

    def __unicode__(self):
        return self.title


class PodcastEpisode(models.Model):
    podcast = models.ForeignKey(Podcast)
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=100)
    file = models.FileField(upload_to='podcasts')
    image = models.ImageField(upload_to='images/podcasts')
    pub_date = models.DateTimeField()
    comments = generic.GenericRelation(Comment, object_id_field='object_pk')
    site = models.ForeignKey(Site)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return self.title

    @property
    def site(self):
        return self.podcast.site
