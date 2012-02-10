from django import forms

import reversion

from proto.core.admin import FileBrowseField
from proto.wiki.models import WikiPage


class WikiPageAdminForm(forms.ModelForm):
    image = FileBrowseField(required=not WikiPage._meta.get_field('image').blank)

    class Meta:
        model = WikiPage


class WikiPageAdmin(reversion.VersionAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug', 'deck']
