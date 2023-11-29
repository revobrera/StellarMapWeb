from decouple import config
from django.shortcuts import redirect, render
from django.urls import reverse

def redirect_to_search_view(request):

    # Redirect to the search_view view
    return redirect(reverse('webApp:search_view'))

def search_view(request):
  context = {
    'search_variable': 'Hello World!',
    'ENV': config('SENTRY_DSN_VUE'),
    'SENTRY_DSN_VUE': config('SENTRY_DSN_VUE')
  }
  return render(request, 'webApp/search.html', context)
