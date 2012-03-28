from django import forms
from django.contrib import admin

from proto.common.admin import FileBrowseField
from proto.news.models import Article


class ArticleAdminForm(forms.ModelForm):
    image = FileBrowseField(required=not Article._meta.get_field('image').blank)

    class Meta:
        model = Article


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    date_heirarchy = 'pub_date'
    list_display = ['title', 'author', 'status', 'pub_date']
    actions = ['make_published']
    raw_id_fields = ('tags',)
    autocomplete_lookup_fields = {
        'm2m': ['tags'],
    }

    class Media:
        js = [
            'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            'js/tinymce_setup.js'
        ]


def make_published(self, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "1 article was"
    else:
        message_bit = "%s articles were" % rows_updated
    self.message_user(request, "%s successfully marked as published." % message_bit)
make_published.short_description = "Mark selected articles as published"


admin.site.register(Article, ArticleAdmin)
