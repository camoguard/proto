from django.db import models

from proto.wiki.models import Wiki


class Game(Wiki):
    release_date = models.DateField(null=True, blank=True)
    platforms = models.ManyToManyField('Platform', null=True, blank=True)
    developers = models.ManyToManyField('Company', related_name='developed_game_set', null=True, blank=True)
    publishers = models.ManyToManyField('Company', related_name='published_game_set', null=True, blank=True)
    genres = models.ManyToManyField('Genre', null=True, blank=True)
    themes = models.ManyToManyField('Theme', null=True, blank=True)


# class Release(models.Model):
#     REGION_CHOICES = (
#         ('NA', 'North America'),
#         ('EU', 'Europe'),
#         ('JP', 'Japan'),
#         ('AU', 'Australia'),
#     )

#     DATE_PRECISION_CHOICES = (
#         ('DAY', 'Day'),
#         ('QUARTER', 'Quarter'),
#         ('HALFYEAR', 'Half-year'),
#         ('YEAR', 'Year'),
#     )

    # RATING_CHOICES = (
    #     ('ESRB (North America)', (
    #             ('ESRB:EC', 'Early Childhood'),
    #             ('ESRB:E', 'Everyone (or K-A)'),
    #             ('ESRB:E10+', 'Everyone 10+'),
    #             ('ESRB:T', 'Teen'),
    #             ('ESRB:M', 'Mature'),
    #             ('ESRB:AO', 'Adults Only'),
    #         )
    #     ),
    #     ('BBFC (Europe)', (
    #             ('BBFC:U', 'Universal'),
    #             ('BBFC:PG', 'Parental Guidance'),
    #             ('BBFC:12', '12'),
    #             ('BBFC:15', '15'),
    #             ('BBFC:18', '18'),
    #         )
    #     ),
    #     ('PEGI (Europe)', (
    #             ('PEGI:3', '3'),
    #             ('PEGI:7', '7'),
    #             ('PEGI:12', '12'),
    #             ('PEGI:16', '16'),
    #             ('PEGI:18', '18'),
    #         )
    #     ),
    #     ('CERO (Japan)', (
    #             ('CERO:A', 'A (or All Ages)'),
    #             ('CERO:B', 'B (or 12+)'),
    #             ('CERO:C', 'C (or 15+)'),
    #             ('CERO:D', 'D'),
    #             ('CERO:Z', 'Z (or 18+)'),
    #         )
    #     ),
    #     ('ACB (Australia)', (
    #             ('ACB:G', 'G'),
    #             ('ACB:PG', 'PG'),
    #             ('ACB:M', 'M (or M15+)'),
    #             ('ACB:MA15+', 'MA15+'),
    #             ('ACB:R18+', 'R18+'),
    #             ('ACB:X18+', 'X18+'),
    #         )
    #     ),
    # )

    # game = models.ForeignKey('Game')
    # image = models.ImageField(upload_to='images/wiki/%s' % game.pk, null=True, blank=True)
    # region = models.CharField(max_length=3, choices=REGION_CHOICES)
    # platform = models.ForeignKey('Platform')
    # release_date = models.DateField(null=True, blank=True)
    # date_precision = models.CharField(max_length=8, choices=DATE_PRECISION_CHOICES, default='DAY')
    # # rating = models.CharField(max_length=10, choices=RATING_CHOICES, null=True, blank=True)

    # class Meta:
    #     unique_together = ('platform', 'region')


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
