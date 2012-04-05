from django.views.generic import DetailView, ListView

from proto.videos.models import Video


class VideoListView(ListView):
    """
    Displays a list of all the videos.
    """
    queryset = Video.public_objects.all()


class VideoDetailView(DetailView):
    """
    Displays a single video.
    """
    queryset = Video.public_objects.all()
