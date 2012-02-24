from django import forms

import reversion

from proto.common.admin import FileBrowseField
from proto.wiki.models import Wiki


class WikiAdminForm(forms.ModelForm):
    image = FileBrowseField(required=not Wiki._meta.get_field('image').blank)

    class Meta:
        model = Wiki


class WikiAdmin(reversion.VersionAdmin):
    list_display = ['name', 'slug', 'deck']
