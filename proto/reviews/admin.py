from django.contrib import admin
from django import forms

from proto.common.admin import FileBrowseField
from proto.reviews.models import Review


class ReviewAdminForm(forms.ModelForm):
    image = FileBrowseField(required=not Review._meta.get_field('image').blank)

    class Meta:
        model = Review


class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    date_heirarchy = 'pub_date'
    list_display = ['title', 'author', 'status', 'pub_date']
    actions = ['make_published']
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }

    class Media:
        js = [
            'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            'js/tinymce_setup.js'
        ]

def make_published(self, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "1 review was"
    else:
        message_bit = "%s reviews were" % rows_updated
    self.message_user(request, "%s successfully marked as published." % message_bit)
make_published.short_description = "Mark selected reviews as published"


admin.site.register(Review, ReviewAdmin)
