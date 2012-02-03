from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models

class Review(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    )

    content_type = models.ForeignKey(ContentType, limit_choices_to = {'model__in': ['game', 'dlc']})
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    author = models.ForeignKey(User, limit_choices_to = {'is_staff': True})
    deck = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='images/reviews')
    pub_date = models.DateTimeField('Publish date')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    comments = generic.GenericRelation(Comment, object_id_field='object_pk')
    sites = models.ManyToManyField(Site)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    on_site = CurrentSiteManager()

    def __unicode__(self):
        return self.title

    @property
    def title(self):
        return '%s Review' % self.content_object