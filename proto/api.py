from tastypie.resources import ModelResource

from proto.games.models import Game


class GameResource(ModelResource):
    class Meta:
        queryset = Game.objects.all()
        resource_name = 'game'
