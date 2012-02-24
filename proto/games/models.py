from django.db import models

from proto.wiki.models import Wiki


class Game(Wiki):
    release_date = models.DateField(null=True, blank=True)
    platforms = models.ManyToManyField('Platform', null=True, blank=True)
    developers = models.ManyToManyField('Company', related_name='developed_game_set', null=True, blank=True)
    publishers = models.ManyToManyField('Company', related_name='published_game_set', null=True, blank=True)
    genres = models.ManyToManyField('Genre', null=True, blank=True)
    themes = models.ManyToManyField('Theme', null=True, blank=True)


class Platform(Wiki):
    release_date = models.DateField(null=True, blank=True)
    company = models.ForeignKey('Company')
    abbreviation = models.CharField(max_length=10, null=True, blank=True)


class Franchise(Wiki):
    games = models.ManyToManyField('Game')


class Character(Wiki):
    games = models.ManyToManyField('Game')


class DLC(Wiki):
    game = models.ForeignKey('Game')
    platforms = models.ManyToManyField('Platform')

    class Meta:
        verbose_name = 'DLC'
        verbose_name_plural = 'DLC'


class Company(Wiki):

    class Meta:
        verbose_name_plural = 'companies'


class Genre(Wiki):
    pass


class Theme(Wiki):
    pass
