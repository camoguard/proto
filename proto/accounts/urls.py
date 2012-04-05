from django.conf.urls import patterns, url

from proto.accounts.views import UserProfileDetailView


urlpatterns = patterns('proto.accounts.views',
    url(r'^(?P<username>[-\w]+)/$', UserProfileDetailView.as_view(), name='user-detail')
)
