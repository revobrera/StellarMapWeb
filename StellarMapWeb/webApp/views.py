from django.shortcuts import redirect, render


def redirect_to_search_view(request):

    # Redirect to the search_view view
    return redirect('search_view')

def search_view(request):
  context = {
    'search_variable': 'Hello World!'
  }
  return render(request, 'webApp/search.html', context)
