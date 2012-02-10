from django.views.generic import DetailView
from django.views.generic.dates import ArchiveIndexView, DayArchiveView, MonthArchiveView, YearArchiveView

from proto.news.models import Article


class ArticleDetailView(DetailView):
    queryset = Article.on_site.all()


class ArticleIndexView(ArchiveIndexView):
    queryset = Article.on_site.all()
    date_field = 'pub_date'


class ArticleYearView(YearArchiveView):
    queryset = Article.on_site.all()
    date_field = 'pub_date'


class ArticleMonthView(MonthArchiveView):
    queryset = Article.on_site.all()
    date_field = 'pub_date'


class ArticleDayView(DayArchiveView):
    queryset = Article.on_site.all()
    date_field = 'pub_date'
