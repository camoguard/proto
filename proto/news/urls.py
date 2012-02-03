from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView
from proto.news.models import Article

urlpatterns = patterns('proto.news.views',
    (r'^$', ListView.as_view(model=Article)),
)
