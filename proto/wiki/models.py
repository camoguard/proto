from django.contrib.contenttypes.models import ContentType
from django.db import models

class WikiPage(models.Model):
    " Wiki object models should subclass this model "
    name = models.CharField(max_length=70)
    deck = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/wiki', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/wiki/%s/%s' % (self.__class__.__name__.lower(), self.pk)

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains',)

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)
