from django.contrib.contenttypes import generic
from django.db import models
from proto.reviews.models import Review
from proto.core.fields import FuzzyDateField

class Game(models.Model):
    title = models.CharField(max_length=100)
    release_date = FuzzyDateField()
    platforms = models.ManyToManyField('Platform')
    developers = models.ManyToManyField('Company', related_name='developed_game_set')
    publishers = models.ManyToManyField('Company', related_name='published_game_set')
    genres = models.ManyToManyField('Genre')
    themes = models.ManyToManyField('Theme')
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.title

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains",)


class Platform(models.Model):
    name = models.CharField(max_length=50)
    release_date = models.DateField()
    company = models.ForeignKey('Company')
    abbreviation = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.name


class DLC(models.Model):
    title = models.CharField(max_length=100)
    game = models.ForeignKey(Game)
    platforms = models.ManyToManyField(Platform)

    class Meta:
        verbose_name = 'DLC'
        verbose_name_plural = 'DLC'

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains",)


class Company(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
