from django.contrib import admin
from django import forms

from proto.core.admin import FileBrowseField
from proto.podcasts.models import Podcast, Episode

class PodcastAdminForm(forms.ModelForm):
    image = FileBrowseField()  # required=not Podcast._meta.get_field('image').blank

    class Meta:
        model = Podcast


class PodcastAdmin(admin.ModelAdmin):
    form = PodcastAdminForm




class EpisodeAdminForm(forms.ModelForm):
    image = FileBrowseField()
    file = FileBrowseField()

    class Meta:
        model = Episode


class EpisodeAdmin(admin.ModelAdmin):
    form = EpisodeAdminForm


admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Episode, EpisodeAdmin)
