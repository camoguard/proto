from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.files.storage import default_storage

from filebrowser.sites import site
from filebrowser.storage import S3BotoStorageMixin
from tastypie.api import Api

from proto.games.api import GameResource, PlatformResource, FranchiseResource, CharacterResource, \
    DLCResource, CompanyResource, GenreResource, ThemeResource
from proto.news.api import ArticleResource


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(GameResource())
v1_api.register(PlatformResource())
v1_api.register(FranchiseResource())
v1_api.register(CharacterResource())
v1_api.register(DLCResource())
v1_api.register(CompanyResource())
v1_api.register(GenreResource())
v1_api.register(ThemeResource())
v1_api.register(ArticleResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'proto.views.home', name='home'),
    # url(r'^proto/', include('proto.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/$', 'proto.accounts.views.profile', name='profile'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^comments/', include('proto.comments.urls')),
    url(r'^news/', include('proto.news.urls')),
    url(r'^forums/', include('proto.forums.urls')),
    url(r'^videos/', include('proto.videos.urls')),
    url(r'^wiki/', include('proto.wiki.urls')),

    url(r'^search/', include('haystack.urls')),
    url(r'^search/autocomplete/$', 'proto.views.ajax_autocomplete', name='ajax-autocomplete'),
    url(r'^api/', include(v1_api.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    if S3BotoStorageMixin not in default_storage.__class__.__bases__:
        default_storage.__class__.__bases__ += (S3BotoStorageMixin,)

    site.storage = default_storage
