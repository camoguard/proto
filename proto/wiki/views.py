from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

import reversion
from reversion.helpers import generate_patch_html
from reversion.models import Version


class WikiDetailView(DetailView):
    def get_queryset(self):
        wiki_class = get_object_or_404(ContentType, model=self.kwargs['model']).model_class()
        self.queryset = wiki_class.objects.all()
        return super(WikiDetailView, self).get_queryset()


class WikiListView(ListView):
    def get_queryset(self):
        wiki_class = get_object_or_404(ContentType, model=self.kwargs['model']).model_class()
        self.queryset = wiki_class.objects.all()
        return super(WikiListView, self).get_queryset()


class WikiUpdateView(UpdateView):
    def get_queryset(self):
        wiki_class = get_object_or_404(ContentType, model=self.kwargs['model']).model_class()
        self.queryset = wiki_class.objects.all()
        return super(WikiUpdateView, self).get_queryset()

    def post(self, request, *args, **kwargs):
        with reversion.create_revision():
            reversion.set_user(request.user)
            if 'comment' in request.POST:
                reversion.set_comment(request.POST['comment'])
            return super(WikiUpdateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WikiUpdateView, self).dispatch(*args, **kwargs)


class WikiCreateView(CreateView):
    def get_queryset(self):
        self.model = get_object_or_404(ContentType, model=self.kwargs['model']).model_class()
        return super(WikiCreateView, self).get_queryset()

    def post(self, request, *args, **kwargs):
        with reversion.create_revision():
            reversion.set_user(request.user)
            if 'comment' in request.POST:
                reversion.set_comment(request.POST['comment'])
            return super(WikiCreateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        permission = 'can_create_%s' % kwargs['model']
        if not args[0].user.has_perm(permission):
            return HttpResponseForbidden('You do not have permission to create a %s.' % kwargs['model'])
        return super(WikiCreateView, self).dispatch(*args, **kwargs)


class WikiDeleteView(DeleteView):
    def get_queryset(self):
        wiki_class = get_object_or_404(ContentType, model=self.kwargs['model']).model_class()
        self.queryset = wiki_class.objects.all()
        return super(WikiDeleteView, self).get_queryset()

    def post(self, request, *args, **kwargs):
        with reversion.create_revision():
            reversion.set_user(request.user)
            if 'comment' in request.POST:
                reversion.set_comment(request.POST['comment'])
            return super(WikiDeleteView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        permission = 'can_delete_%s' % kwargs['model']
        if not args[0].user.has_perm(permission):
            return HttpResponseForbidden('You do not have permission to delete this %s.' % kwargs['model'])
        return super(WikiDeleteView, self).dispatch(*args, **kwargs)


class VersionListView(ListView):
    def get_queryset(self):
        content_type = get_object_or_404(ContentType, model=self.kwargs['model'])

        # Fetch the revisions for the wiki object using either the pk or slug, depending on what's provided
        if 'slug' in self.kwargs:
            self.wiki_object = content_type.get_object_for_this_type(slug=self.kwargs['slug'])
        else:
            self.wiki_object = content_type.get_object_for_this_type(pk=self.kwargs['pk'])

        self.queryset = reversion.get_for_object(self.wiki_object).select_related('revision__user')
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


def wiki_home(request):
    wiki_list = []
    return render(request, 'wiki/wiki_home.html', {'object_list': wiki_list})
