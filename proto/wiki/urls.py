from django.conf.urls.defaults import patterns, url, include

from proto.wiki.views import WikiDetailView, WikiUpdateView, WikiCreateView, WikiDeleteView, VersionListView


urlpatterns = patterns('proto.wiki.views',
    url(r'^create/(?P<model>\w+)/$', WikiCreateView.as_view(), name='wiki-create'),

    url(r'^(?P<model>\w+)/(?P<pk>\d+)/$', WikiDetailView.as_view(), name='wiki-detail-pk'),
    url(r'^(?P<model>\w+)/(?P<slug>[-\w]+)/$', WikiDetailView.as_view(), name='wiki-detail-slug'),

    url(r'^(?P<model>\w+)/(?P<pk>\d+)/edit/$', WikiUpdateView.as_view(), name='wiki-edit-pk'),
    url(r'^(?P<model>\w+)/(?P<slug>[-\w]+)/edit/$', WikiUpdateView.as_view(), name='wiki-edit-slug'),

    url(r'^(?P<model>\w+)/(?P<pk>\d+)/delete/$', WikiDeleteView.as_view(), name='wiki-delete-pk'),
    url(r'^(?P<model>\w+)/(?P<slug>[-\w]+)/delete/$', WikiDeleteView.as_view(), name='wiki-delete-slug'),

    url(r'^(?P<model>\w+)/(?P<pk>\d+)/history/$', VersionListView.as_view(), name='wiki-history-pk'),
    url(r'^(?P<model>\w+)/(?P<slug>[-\w]+)/history/$', VersionListView.as_view(), name='wiki-history-slug'),

    url(r'^diff/(?P<old_version_pk>\d+)/(?P<new_version_pk>\d+)$', 'diff_view', name='wiki-diff')
)
