from django import forms
from django.contrib import admin

from proto.core.admin import FileBrowseField
from proto.videos.models import Video, VideoCategory

class VideoAdminForm(forms.ModelForm):
    image = FileBrowseField()

    class Meta:
        model = Video


class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    date_heirarchy = 'pub_date'
    list_display = ['title', 'status', 'pub_date']
    actions = ['make_published']

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js'
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