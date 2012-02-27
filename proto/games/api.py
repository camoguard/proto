from tastypie import fields

from proto.games.models import Game, Platform, Franchise, Character, DLC, Company, Genre, Theme
from proto.wiki.api import WikiResource


class GameResource(WikiResource):
    class Meta(WikiResource.Meta):
        queryset = Game.objects.all()


class PlatformResource(WikiResource):
    class Meta(WikiResource.Meta):
        queryset = Platform.objects.all()


class FranchiseResource(WikiResource):
    games = fields.ManyToManyField(GameResource, 'games', full=False)

    class Meta(WikiResource.Meta):
        queryset = Franchise.objects.all()


class CharacterResource(WikiResource):
    class Meta(WikiResource.Meta):
        queryset = Character.objects.all()


class DLCResource(WikiResource):
    class Meta(WikiResource.Meta):
        queryset = DLC.objects.all()


class CompanyResource(WikiResource):
    class Meta(WikiResource.Meta):
        queryset = Company.objects.all()


class GenreResource(WikiResource):
    class Meta(WikiResource.Meta):
        queryset = Genre.objects.all()


class ThemeResource(WikiResource):
    class Meta(WikiResource.Meta):
        queryset = Theme.objects.all()
