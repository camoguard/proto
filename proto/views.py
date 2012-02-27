import json

from django.http import HttpResponse
from django.shortcuts import render

from haystack.query import SearchQuerySet


def home(request):

    return render(request, 'home.html', {})


def ajax_autocomplete(request):
    results = SearchQuerySet().autocomplete(title_auto=request.GET.get('q', '')).values('title', 'model_name', 'pk')
    return HttpResponse(json.dumps(results[:5]), content_type='application/json')
