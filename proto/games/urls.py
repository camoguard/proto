from django.conf.urls.defaults import patterns, url, include

from proto.games.views import GameDetailView, GameUpdateView

urlpatterns = patterns('proto.games.views',
    url(r'^(?P<slug>[-\w]+)/$', GameDetailView.as_view(), name='game-detail'),
    url(r'^(?P<slug>[-\w]+)/edit$', GameUpdateView.as_view(), name='game-update'),
)
