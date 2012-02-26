from django.conf.urls import patterns, url

from proto.news.views import ArticleDetailView, ArticleIndexView, ArticleYearView, ArticleMonthView, ArticleDayView


urlpatterns = patterns('proto.news.views',
    url(r'^(?P<year>\d{4})/$', ArticleYearView.as_view(), name='article-year-archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', ArticleMonthView.as_view(), name='article-month-archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', ArticleDayView.as_view(), name='article-day-archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),
    url(r'^$', ArticleIndexView.as_view(), name='article-index-archive'),
)
