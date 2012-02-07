from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.comments.managers import CommentManager
from django.conf import settings


PATH_SEPARATOR = getattr(settings, 'COMMENT_PATH_SEPARATOR', '/')
PATH_DIGITS = getattr(settings, 'COMMENT_PATH_DIGITS', 10)


class RelatedCommentManager(CommentManager):
    def filter(self, *args, **kwargs):
        return super(RelatedCommentManager, self).select_related('user', 'user__profile').filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        return super(RelatedCommentManager, self).select_related('user', 'user__profile').exclude(*args, **kwargs)

    def all(self):
        return super(RelatedCommentManager, self).select_related('user', 'user__profile').all()


class ThreadedComment(Comment):
    parent = models.ForeignKey('self', null=True, blank=True, default=None, related_name='children')
    last_child = models.ForeignKey('self', null=True, blank=True)
    tree_path = models.TextField(editable=False, db_index=True)

    objects = RelatedCommentManager()

    class Meta(object):
        ordering = ('tree_path',)

    def save(self, *args, **kwargs):
        skip_tree_path = kwargs.pop('skip_tree_path', False)
        super(ThreadedComment, self).save(*args, **kwargs)
        if skip_tree_path:
            return None

        tree_path = unicode(self.pk).zfill(PATH_DIGITS)
        if self.parent:
            tree_path = PATH_SEPARATOR.join((self.parent.tree_path, tree_path))

            self.parent.last_child = self
            ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=self)

        self.tree_path = tree_path
        ThreadedComment.objects.filter(pk=self.pk).update(tree_path=self.tree_path)

    @property
    def depth(self):
        return len(self.tree_path.split(PATH_SEPARATOR))

    @property
    def root_id(self):
        return int(self.tree_path.split(PATH_SEPARATOR)[0])

    @property
    def root_path(self):
        return ThreadedComment.objects.filter(pk__in=self.tree_path.split(PATH_SEPARATOR)[:-1])
