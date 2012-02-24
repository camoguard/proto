from django.db import models

from model_utils.managers import InheritanceManager

from proto.core.models import InheritanceMixIn
from proto.core.fields import AutoSlugField


class Wiki(InheritanceMixIn, models.Model):
    """
    Super class of wiki models.
    This model cannot be instantiated directly; it must be subclassed.
    """
    name = models.CharField(max_length=70)
    slug = AutoSlugField(populate_from='name')
    deck = models.CharField(max_length=100)
    wiki_content = models.TextField()
    image = models.ImageField(upload_to='images/wiki', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = InheritanceManager()

    class Meta:
        unique_together = ('_class', 'slug')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('wiki-detail-slug', (), {
            'model': self._class,
            'slug': self.slug})

    def get_class(self):
        return self._class

    def related_label(self):
        return '%s (%s)' % (self.name, self._class)

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains',)
