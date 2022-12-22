from django.shortcuts import render

def search_view(request):
  context = {
    'search_variable': 'Hello World!'
  }
  return render(request, 'search.html', context)