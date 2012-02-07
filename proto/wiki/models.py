from django.contrib.contenttypes.models import ContentType
from django.db import models

class WikiPage(models.Model):
    name = models.CharField(max_length=70)
    deck = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)
