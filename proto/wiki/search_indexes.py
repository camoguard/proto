from haystack import indexes

from proto.wiki.models import Wiki


class WikiIndex(indexes.SearchIndex):
    """
    Provides standardized search index behavior of :model:`wiki.Wiki` subclasses.
    This class should not be indexed by Haystack.
    """
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='name')
    deck = indexes.CharField(model_attr='deck')
    title_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Wiki

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
