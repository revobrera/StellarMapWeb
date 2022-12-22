from django.urls import path
from webApp import views

app_name = 'webApp'
urlpatterns = [  
    path('search/', views.search_view, name='search_view'),  
]