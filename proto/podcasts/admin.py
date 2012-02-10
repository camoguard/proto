from django.contrib import admin
from django import forms

from proto.core.admin import FileBrowseField
from proto.podcasts.models import Podcast, PodcastEpisode


class PodcastAdminForm(forms.ModelForm):
    image = FileBrowseField(required=not Podcast._meta.get_field('image').blank)

    class Meta:
        model = Podcast


class PodcastAdmin(admin.ModelAdmin):
    form = PodcastAdminForm


class PodcastEpisodeAdminForm(forms.ModelForm):
    image = FileBrowseField(required=not PodcastEpisode._meta.get_field('image').blank)
    file = FileBrowseField(required=not PodcastEpisode._meta.get_field('file').blank)

    class Meta:
        model = PodcastEpisode


class PodcastEpisodeAdmin(admin.ModelAdmin):
    form = PodcastEpisodeAdminForm


admin.site.register(Podcast, PodcastAdmin)
admin.site.register(PodcastEpisode, PodcastEpisodeAdmin)
