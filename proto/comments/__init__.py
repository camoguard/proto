"""
Change the attributes you want to customize
"""

from proto.comments.models import ThreadedComment
from proto.comments.forms import ThreadedCommentForm


def get_model():
    return ThreadedComment


def get_form():
    return ThreadedCommentForm
