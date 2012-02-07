from django.http import Http404
from django.shortcuts import render

from proto.comments.models import ThreadedComment


def ajax_comment_form(request, comment_id):
    if not request.is_ajax():
        raise Http404

    comment = ThreadedComment.objects.get(pk=comment_id)
    object = comment.content_object
    return render(request, 'comments/comment_form.html', {'comment': comment, 'object': object})
