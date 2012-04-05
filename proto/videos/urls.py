from django.conf.urls import patterns, url

from proto.videos.views import VideoDetailView, VideoListView


urlpatterns = patterns('proto.videos.views',
    url(r'^$', VideoListView.as_view(), name='video-list'),
    url(r'^$', VideoDetailView.as_view(), name='video-detail')
)
