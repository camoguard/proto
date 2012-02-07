from django.conf.urls.defaults import patterns, url, include

from proto.wiki.views import VersionListView

urlpatterns = patterns('proto.wiki.views',
    url(r'^(?P<model>\w+)/(?P<object_id>[-\w]+)/history/$', VersionListView.as_view(), name='wiki-history'),
    url(r'^diff/(?P<old_version_pk>\d+)/(?P<new_version_pk>\d+)$', 'diff_view', name='wiki-diff')
)
