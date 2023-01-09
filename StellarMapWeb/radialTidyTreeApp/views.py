from django.shortcuts import redirect, render
from django.urls import reverse


def radial_tidy_tree_view(request):
  context = {
    'radial_tidy_tree_variable': 'Hello World!'
  }
  return render(request, 'webApp/radial_tidy_tree.html', context)