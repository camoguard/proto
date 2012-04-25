from django.contrib.auth.models import User
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models

from sorl.thumbnail import ImageField

from proto.wiki.models import Wiki


class Image(models.Model):
    """
    Stores an image.
    """
    image = ImageField(upload_to='images')
    caption = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    tags = models.ManyToManyField(Wiki, null=True, blank=True)
    site = models.ForeignKey(Site)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    on_site = CurrentSiteManager()

    def __unicode__(self):
        return self.image.name
