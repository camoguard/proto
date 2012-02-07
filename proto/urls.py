from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from filebrowser.sites import site
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'proto.views.home', name='home'),
    # url(r'^proto/', include('proto.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'^accounts/profile/', 'proto.accounts.views.profile', name='profile'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^comments/', include('proto.comments.urls')),
    url(r'^news/', include('proto.news.urls')),
    url(r'^forums/', include('proto.forums.urls')),
    url(r'^games/', include('proto.games.urls')),
    url(r'^wiki/', include('proto.wiki.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )