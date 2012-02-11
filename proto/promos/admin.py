from django.contrib import admin
from django.db import models
from django.forms.widgets import HiddenInput

from filebrowser.base import FileObject
from filebrowser.settings import ADMIN_THUMBNAIL

from proto.promos.models import PromoContainer, Promo


class PromoInline(admin.TabularInline):
    model = Promo
    readonly_fields = ['image_thumbnail']
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }
    sortable_field_name = 'position'
    formfield_overrides = {
        models.PositiveSmallIntegerField: {'widget': HiddenInput},
    }
    max_num = 0

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def image_thumbnail(self, obj):
        image = obj.content_object.image
        if image:
            fb_image = FileObject(image.path)
            if fb_image.filetype == 'Image':
                url = image.url.rsplit('/', 1)[0] + '/' + fb_image.version_generate(ADMIN_THUMBNAIL).filename
                return '<img src="%s" />' % url
        else:
            return '(None)'
    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = "Thumbnail"


class PromoContainerAdmin(admin.ModelAdmin):
    inlines = [PromoInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(PromoContainer, PromoContainerAdmin)
