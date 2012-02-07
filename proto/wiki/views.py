from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

import reversion
from reversion.helpers import generate_patch_html
from reversion.models import Version

class VersionListView(ListView):
    def get_queryset(self):
        content_type = ContentType.objects.get(model=self.kwargs['model'])
        self.wiki_object = content_type.get_object_for_this_type(pk=self.kwargs['object_id'])
        self.queryset = reversion.get_for_object(self.wiki_object)
        self.queryset = self.queryset.select_related('revision__user')
        return super(VersionListView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(VersionListView, self).get_context_data(**kwargs)
        context['wiki_object'] = self.wiki_object
        return context

def diff_view(request, old_version_pk, new_version_pk):
    # Get the two versions to compare
    old_version = Version.objects.get(pk=old_version_pk)
    new_version = Version.objects.get(pk=new_version_pk)

    # Generate and render the diff
    diff_html = generate_patch_html(old_version, new_version, "content", cleanup="semantic")

    return render(request, 'reversion/diff_detail.html', {
        'old_version': old_version,
        'new_version': new_version,
        'diff_html': diff_html
    })


class WikiDetailView(DetailView):
    pass


class WikiUpdateView(UpdateView):
    def post(self, request, *args, **kwargs):
        with reversion.create_revision():
            reversion.set_user(request.user)
            if 'comment' in request.POST:
                reversion.set_comment(request.POST['comment'])
            return super(WikiUpdateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WikiUpdateView, self).dispatch(*args, **kwargs)