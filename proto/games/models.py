from django.db import models

from proto.core.fields import FuzzyDateField
from proto.wiki.models import WikiPage


class Game(WikiPage):
    release_date = FuzzyDateField(null=True, blank=True)
    platforms = models.ManyToManyField('Platform', null=True, blank=True)
    developers = models.ManyToManyField('Company', related_name='developed_game_set', null=True, blank=True)
    publishers = models.ManyToManyField('Company', related_name='published_game_set', null=True, blank=True)
    genres = models.ManyToManyField('Genre', null=True, blank=True)
    themes = models.ManyToManyField('Theme', null=True, blank=True)


class Platform(WikiPage):
    release_date = models.DateField()
    company = models.ForeignKey('Company')
    abbreviation = models.CharField(max_length=10, blank=True, null=True)


class Franchise(WikiPage):
    games = models.ManyToManyField('Game')


class Character(WikiPage):
    games = models.ManyToManyField('Game')


class DLC(WikiPage):
    game = models.ForeignKey('Game')
    platforms = models.ManyToManyField('Platform')

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
