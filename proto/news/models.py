from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models

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
    slug = models.SlugField()
    body = models.TextField()
    image = models.ImageField(upload_to='images/news')
    pub_date = models.DateTimeField('Publish date')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    comments = generic.GenericRelation(Comment, object_id_field='object_pk')
    site = models.ForeignKey(Site)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('article-detail', (), {
            'year': self.pub_date.year,
            'month': self.pub_date.strftime('%b'),
            'day': self.pub_date.strftime('%d'),
            'slug': self.slug})