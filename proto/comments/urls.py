from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('proto.comments.views',
    url(r'^comments/(?P<comment_id>\d+)/form/$', 'ajax_comment_form', name='ajax-comment-form')
)
