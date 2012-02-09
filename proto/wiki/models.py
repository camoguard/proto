from django.db import models


class WikiPage(models.Model):
    "Abstract base model for wiki models"
    name = models.CharField(max_length=70)
    slug = models.SlugField(unique=True)
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

    @property
    def wiki_type(self):
        return self.__class__.__name__.lower()

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains',)
