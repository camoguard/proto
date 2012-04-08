from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

import reversion
from reversion.helpers import generate_patch_html
from reversion.models import Version

from proto.wiki.models import Wiki


class WikiDetailView(DetailView):
    """
    Displays an individual :model:`wiki.Wiki`.
    """
    def get_template_names(self):
        names = super(WikiDetailView, self).get_template_names()
        names.append('wiki/wiki_detail.html')
        return names

    def get_queryset(self):
        wiki_model = get_object_or_404(ContentType, model=self.kwargs['model']).model_class()
        self.queryset = wiki_model.objects.all()
        return super(WikiDetailView, self).get_queryset()


class WikiListView(ListView):
    """
    Displays a list of :model:`wiki.Wiki` of a specific subclass.
    """
    def get_template_names(self):
        names = super(WikiListView, self).get_template_names()
        names.append('wiki/wiki_list.html')
        return names

    def get_queryset(self):
        wiki_model = get_object_or_404(ContentType, model=self.kwargs['model']).model_class()
        self.queryset = wiki_model.objects.all()
        return super(WikiListView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(WikiListView, self).get_context_data(**kwargs)
        context['model'] = self.kwargs['model']
        return context


class WikiUpdateView(UpdateView):
    """
    Displays the form for editing an existing :model:`wiki.Wiki`.
    """
    def get_template_names(self):
        names = super(WikiUpdateView, self).get_template_names()
        names.append('wiki/wiki_form.html')
        return names

    def get_queryset(self):
        wiki_model = get_object_or_404(ContentType, model=self.kwargs['model']).model_class()
        self.queryset = wiki_model.objects.all()
        return super(WikiUpdateView, self).get_queryset()

    def get_form(self, form_class):
        # Don't let non-staff users change the names of existing wiki pages as
        # this could lead to all sorts of trouble
        form = super(WikiUpdateView, self).get_form(form_class)
        if not self.request.user.is_staff:
            del form.fields['name']
        return form

    def post(self, request, *args, **kwargs):
        with reversion.create_revision():
            reversion.set_user(request.user)
            if 'comment' in request.POST and request.POST['comment']:
                reversion.set_comment(request.POST['comment'])
            return super(WikiUpdateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WikiUpdateView, self).dispatch(*args, **kwargs)


class WikiCreateView(CreateView):
    """
    Displays the form for creating a new :model:`wiki.Wiki`.
    """
    def get_template_names(self):
        names = super(WikiCreateView, self).get_template_names()
        names.append('wiki/wiki_form.html')
        return names

    def get_queryset(self):
        self.model = get_object_or_404(ContentType, model=self.kwargs['model']).model_class()
        return super(WikiCreateView, self).get_queryset()

    def post(self, request, *args, **kwargs):
        with reversion.create_revision():
            reversion.set_user(request.user)
            if 'comment' in request.POST and request.POST['comment']:
                reversion.set_comment(request.POST['comment'])
            return super(WikiCreateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WikiCreateView, self).get_context_data(**kwargs)
        context['model'] = self.model
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        permission = 'can_create_%s' % kwargs['model']
        if not args[0].user.has_perm(permission):
            return HttpResponseForbidden('You do not have permission to create a %s.' % kwargs['model'])
        return super(WikiCreateView, self).dispatch(*args, **kwargs)


class WikiDeleteView(DeleteView):
    """
    Displays the page for deleting an individual :model:`wiki.Wiki`.
    """
    def get_template_names(self):
        names = super(WikiDeleteView, self).get_template_names()
        names.append('wiki/wiki_confirm_delete.html')
        return names

    def get_queryset(self):
        wiki_model = get_object_or_404(ContentType, model=self.kwargs['model']).model_class()
        self.queryset = wiki_model.objects.all()
        return super(WikiDeleteView, self).get_queryset()

    def post(self, request, *args, **kwargs):
        with reversion.create_revision():
            reversion.set_user(request.user)
            if 'comment' in request.POST and request.POST['comment']:
                reversion.set_comment(request.POST['comment'])
            return super(WikiDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "The %s <em>%s</em> was deleted." % (self.kwargs['model'], self.object.name))
        return reverse('wiki-list', kwargs={'model': self.kwargs['model']})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        permission = 'can_delete_%s' % kwargs['model']
        if not args[0].user.has_perm(permission):
            return HttpResponseForbidden('You do not have permission to delete this %s.' % kwargs['model'])
        return super(WikiDeleteView, self).dispatch(*args, **kwargs)


class WikiHistoryView(ListView):
    """
    Displays the edit history of an individual :model:`wiki.Wiki`.
    """
    template_name = 'wiki/wiki_history.html'

    def get_queryset(self):
        content_type = get_object_or_404(ContentType, model=self.kwargs['model'])

        # Fetch the revisions for the wiki object using either the pk or slug,
        # depending on what's provided
        if 'slug' in self.kwargs:
            self.wiki_object = content_type.get_object_for_this_type(slug=self.kwargs['slug'])
        else:
            self.wiki_object = content_type.get_object_for_this_type(pk=self.kwargs['pk'])

        self.queryset = reversion.get_for_object(self.wiki_object).select_related('revision__user')
        return super(WikiHistoryView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(WikiHistoryView, self).get_context_data(**kwargs)
        context['wiki_object'] = self.wiki_object
        return context


def process_wiki_history_form(request):
    old_version_pk = request.GET.get('old-version')
    new_version_pk = request.GET.get('new-version')
    return redirect('wiki-diff', old_version_pk=old_version_pk, new_version_pk=new_version_pk)


def wiki_diff(request, old_version_pk, new_version_pk):
    """
    Displays a diff between two :model:`wiki.Wiki` versions.
    """
    # Get the two versions to compare
    old_version = Version.objects.select_related('revision__user', 'revision__comment').get(pk=old_version_pk)
    new_version = Version.objects.select_related('revision__user', 'revision__comment').get(pk=new_version_pk)

    # Don't generate a diff if the versions belong to different wiki objects
    if old_version.object_id != new_version.object_id:
        raise Http404

    wiki_object = new_version.object.get_object()

    diff_html = {}
    for field, value in new_version.field_dict.items():
        real_field = wiki_object._meta.get_field_by_name(field)[0]

        # Only the PKs of any foreign keys are stored in versions
        # We need to replace these keys with the names of the objects to show meaningful values to the user
        if real_field.get_internal_type() in ['ManyToManyField', 'ForeignKey']:
            if isinstance(value, list):  # m2m
                old_pks = old_version.field_dict[field]
                new_pks = new_version.field_dict[field]
            else:  # fk
                old_pks = [old_version.field_dict[field]]
                new_pks = [new_version.field_dict[field]]

            fk_objects = Wiki.objects.in_bulk(set(old_pks + new_pks))

            old_fk_names = [fk_objects[int(fk)].name for fk in old_pks]
            old_version.field_dict[field] = ', '.join(old_fk_names)

            new_fk_names = [fk_objects[int(fk)].name for fk in new_pks]
            new_version.field_dict[field] = ', '.join(new_fk_names)

        if real_field.editable and field not in ['id', 'wiki_ptr']:
            diff_html[real_field.verbose_name] = generate_patch_html(old_version, new_version, field, cleanup='semantic')

    return render(request, 'wiki/wiki_diff.html', {
        'old_version': old_version,
        'new_version': new_version,
        'diff_html': diff_html,
        'wiki_object': wiki_object
    })


def wiki_home(request):
    wiki_list = Wiki.objects.all()
    return render(request, 'wiki/wiki_home.html', {'object_list': wiki_list})
