from proto.games.models import Game
from proto.wiki.views import WikiDetailView, WikiUpdateView

class GameDetailView(WikiDetailView):
    queryset = Game.objects.all().select_related('wiki_page')


class GameUpdateView(WikiUpdateView):
    queryset = Game.objects.all()
