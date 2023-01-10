from django.urls import path
from radialTidyTreeApp import views

app_name = 'radialTidyTreeApp'
urlpatterns = [
    path('tree/', views.radial_tidy_tree_view, name='radial_tidy_tree_view'),  
]