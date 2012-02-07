from django.db import models

from proto.core.fields import FuzzyDateField
from proto.wiki.models import WikiPage

class Game(WikiPage):
    release_date = FuzzyDateField()
    platforms = models.ManyToManyField('Platform')
    developers = models.ManyToManyField('Company', related_name='developed_game_set')
    publishers = models.ManyToManyField('Company', related_name='published_game_set')
    genres = models.ManyToManyField('Genre')
    themes = models.ManyToManyField('Theme')
    slug = models.SlugField(unique=True)


class Platform(WikiPage):
    release_date = models.DateField()
    company = models.ForeignKey('Company')
    abbreviation = models.CharField(max_length=10, blank=True, null=True)


class DLC(WikiPage):
    game = models.ForeignKey(Game)
    platforms = models.ManyToManyField(Platform)

    class Meta:
        verbose_name = 'DLC'
        verbose_name_plural = 'DLC'


class Company(WikiPage):
    pass

    class Meta:
        verbose_name_plural = 'companies'


class Genre(WikiPage):
    pass


class Theme(WikiPage):
    pass
