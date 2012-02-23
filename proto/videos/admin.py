from django import forms
from django.contrib import admin

from proto.core.admin import FileBrowseField
from proto.videos.models import Video, VideoCategory


class VideoAdminForm(forms.ModelForm):
    image = FileBrowseField(required=not Video._meta.get_field('image').blank)
    file = FileBrowseField(required=not Video._meta.get_field('file').blank)

    class Meta:
        model = Video


class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    date_heirarchy = 'pub_date'
    list_display = ['title', 'status', 'pub_date']
    actions = ['make_published']
    raw_id_fields = ('tags',)
    autocomplete_lookup_fields = {
        'm2m': ['tags']
    }

    class Media:
        js = [
            'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            'js/tinymce_setup.js'
        ]


def make_published(self, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "1 video was"
    else:
        message_bit = "%s videos were" % rows_updated
    self.message_user(request, "%s successfully marked as published." % message_bit)
make_published.short_description = "Mark selected videos as published"


class VideoCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Video, VideoAdmin)
admin.site.register(VideoCategory, VideoCategoryAdmin)
