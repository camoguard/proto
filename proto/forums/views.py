from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from proto.forums.forms import ThreadForm, PostInlineFormSet, PostForm
from proto.forums.models import Forum, Thread, Post, FORUM_LAST_POST_KEY, THREAD_LAST_POST_KEY

class ForumListView(ListView):
    # Retrieve the number of threads and posts in each forum for display with the queryset
    queryset = Forum.on_site.all().annotate(num_threads=Count('thread', distinct=True),
                                            num_posts=Count('thread__post', distinct=True))


class ThreadListView(ListView):
    def get_queryset(self):
        forum = get_object_or_404(Forum, slug=self.kwargs['forum_slug'], site=settings.SITE_ID)
        return Thread.objects.filter(forum=forum).select_related('creator', 'forum').annotate(num_posts=Count('post'))

    def get_context_data(self, **kwargs):
        context = super(ThreadListView, self).get_context_data(**kwargs)
        context['forum_slug'] = self.kwargs['forum_slug']
        return context


class PostListView(ListView):
    def get_queryset(self):
        thread = get_object_or_404(Thread, pk=self.kwargs['thread_id'], forum__site=settings.SITE_ID)
        return Post.objects.filter(thread=thread).select_related('creator')

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['forum_slug'] = self.kwargs['forum_slug']
        context['thread_id'] = self.kwargs['thread_id']
        context['post_form'] = PostForm()
        return context


@login_required
def create_thread(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug, site=settings.SITE_ID)

    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            # Sets the forum and creator of the thread, which aren't part of the form
            form.instance.forum = forum
            form.instance.creator = request.user
            thread = form.save(commit=False)

            # Uses an inline formset in order to create the thread and its first post using the same form
            post_formset = PostInlineFormSet(request.POST, instance=thread)
            if post_formset.is_valid():
                for form in post_formset.forms:
                    # Sets the creator of the post
                    form.instance.creator = request.user
                thread.save()
                post_formset.save()

                messages.success(request, "Your thread '%s' was created." % thread.title)

            return redirect(thread.get_absolute_url())
    else:
        form = ThreadForm()
        post_formset = PostInlineFormSet(instance=Thread())

    return render(request, 'forums/thread_form.html', {
        'form': form,
        'post_formset': post_formset,
    })


@login_required
@require_POST
def process_post_form(request, forum_slug, thread_id):
    # Makes sure that the user is posting to an existing thread
    thread = get_object_or_404(Thread.objects.select_related('forum'),
                                pk=thread_id, forum__slug=forum_slug, forum__site=settings.SITE_ID)

    form = PostForm(request.POST)
    if form.is_valid():
        # Sets the thread and creator of the post, which aren't part of the form
        form.instance.thread = thread
        form.instance.creator = request.user
        form.save()
        # Saves the thread without any changes so that its modified field gets updated
        # and it gets moved to the top of its forum's thread list
        thread.save()

        # Invalidate the last post cached for this post's thread and forum
        cache.delete(THREAD_LAST_POST_KEY % thread.pk)
        cache.delete(FORUM_LAST_POST_KEY % thread.forum.pk)

        messages.success(request, "Your post was successful.")

    return redirect(thread.get_absolute_url())
