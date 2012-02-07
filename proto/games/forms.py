from django.forms import ModelForm

from proto.games.models import Game

class GameForm(ModelForm):

    class Meta:
        model = Game

