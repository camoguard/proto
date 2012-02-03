from django.conf.urls.defaults import patterns, url, include

from proto.forums.views import ForumListView, ThreadListView, PostListView

urlpatterns = patterns('proto.forums.views',
    url(r'^(?P<forum_slug>[-\w]+)/create-thread/$', 'create_thread', name='create_thread'),
    url(r'^(?P<forum_slug>[-\w]+)/(?P<thread_id>\d+)/process-post/$', 'process_post_form', name='process_post_form'),
    url(r'^(?P<forum_slug>[-\w]+)/(?P<thread_id>\d+)/$', PostListView.as_view(), name='view_posts'),
    url(r'^(?P<forum_slug>[-\w]+)/$', ThreadListView.as_view(), name='view_threads'),
    url(r'^$', ForumListView.as_view(), name='view_forums')
)
