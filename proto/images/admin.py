from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from proto.images.models import Image


class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
