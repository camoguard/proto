from haystack import indexes

from proto.news.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    deck = indexes.CharField(model_attr='deck')
    title_autocomplete = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Article

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().public_objects.all()
