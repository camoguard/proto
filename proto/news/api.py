from tastypie.resources import ALL

from proto.common.api import SearchModelResource
from proto.news.models import Article


class ArticleResource(SearchModelResource):
    """
    Provides standardized API behavior of :model:`wiki.Wiki` subclasses.
    This class should not be registered with Tastypie.
    """
    class Meta:
        queryset = Article.public_objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        include_absolute_url = True
        filtering = {
            'slug': ('exact', 'startswith',),
            'title': ALL,
        }
