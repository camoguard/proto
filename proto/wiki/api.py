from django.conf.urls.defaults import patterns, include, url
from tastypie.resources import ALL

from proto.common.api import SearchModelResource


class WikiResource(SearchModelResource):
    """
    Provides standardized API behavior of :model:`wiki.Wiki` subclasses.
    This class should not be registered with Tastypie.
    """
    class Meta:
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {
            'slug': ('exact', 'startswith',),
            'name': ALL,
        }
