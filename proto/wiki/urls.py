from django.conf.urls import patterns, url

from proto.wiki.views import WikiCreateView, WikiListView, WikiDetailView, WikiUpdateView, \
                            WikiDeleteView, WikiHistoryView


urlpatterns = patterns('proto.wiki.views',
    url(r'^diff/$', 'process_wiki_history_form', name='process-wiki-history-form'),
    url(r'^diff/(?P<old_version_pk>\d+)/(?P<new_version_pk>\d+)/$', 'wiki_diff', name='wiki-diff'),

    url(r'^create/(?P<model>\w+)/$', WikiCreateView.as_view(), name='wiki-create'),

    url(r'^(?P<model>\w+)/$', WikiListView.as_view(), name='wiki-list'),

    # url(r'^(?P<model>\w+)/(?P<pk>\d+)/$', WikiDetailView.as_view(), name='wiki-detail-pk'),
    url(r'^(?P<model>\w+)/(?P<slug>[-\w]+)/$', WikiDetailView.as_view(), name='wiki-detail-slug'),

    # url(r'^(?P<model>\w+)/(?P<pk>\d+)/edit/$', WikiUpdateView.as_view(), name='wiki-edit-pk'),
    url(r'^(?P<model>\w+)/(?P<slug>[-\w]+)/edit/$', WikiUpdateView.as_view(), name='wiki-edit-slug'),

    # url(r'^(?P<model>\w+)/(?P<pk>\d+)/delete/$', WikiDeleteView.as_view(), name='wiki-delete-pk'),
    url(r'^(?P<model>\w+)/(?P<slug>[-\w]+)/delete/$', WikiDeleteView.as_view(), name='wiki-delete-slug'),

    # url(r'^(?P<model>\w+)/(?P<pk>\d+)/history/$', WikiHistoryView.as_view(), name='wiki-history-pk'),
    url(r'^(?P<model>\w+)/(?P<slug>[-\w]+)/history/$', WikiHistoryView.as_view(), name='wiki-history-slug'),

    url(r'^$', 'wiki_home', name='wiki-home'),
)
