from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin

from proto.comments.models import ThreadedComment


class ThreadedCommentsAdmin(CommentsAdmin):
    list_display = ('name', 'content_type', 'object_pk', 'parent',
                    'ip_address', 'submit_date', 'is_public', 'is_removed')
    search_fields = ('comment', 'user__username', 'user_name',
                     'user_email', 'user_url', 'ip_address')
    raw_id_fields = ('parent',)

admin.site.register(ThreadedComment, ThreadedCommentsAdmin)
