from django import forms

from filebrowser.base import FileObject
from filebrowser.fields import FileBrowseWidget as fb_FileBrowseWidget
from filebrowser.sites import site as filebrowser_site


class FileBrowseWidget(fb_FileBrowseWidget):
    def render(self, name, value, attrs={}):
        if not value:
            value = ""
        else:
            value = FileObject(value.name, site=self.site)
        return super(FileBrowseWidget, self).render(name, value, attrs)


class FileBrowseField(forms.CharField):
    # Use a CharField, not an ImageField or FileField, since filebrowser
    # is handling any file uploading
    widget = FileBrowseWidget(attrs={'filebrowser_site': filebrowser_site})
