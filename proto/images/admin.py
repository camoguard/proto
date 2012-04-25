from django.contrib import admin
from images.models import Image
from sorl.thumbnail.admin import AdminImageMixin


class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
