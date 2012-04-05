from django.shortcuts import render
from django.views.generic import DetailView

from proto.accounts.models import UserProfile


def profile(request):

    return render(request, 'profile.html', {})


class UserProfileDetailView(DetailView):
    """
    Displays a single user profile.
    """
    queryset = UserProfile.objects.all()

    def get_object(self):
        object = self.queryset.get(user__username=self.kwargs['username'])
        return object
