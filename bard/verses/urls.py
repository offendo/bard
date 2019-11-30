from django.urls import path
from . import views

urlpatterns = [
        path('verses', views.story_list_view, name='list'),
        path('verses/story', views.story_view, name='story'),
]

