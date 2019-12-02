from django.urls import path
from . import views

urlpatterns = [
        path('verses', views.verse_list_view, name='list'),
        path('verses/add_genre', views.verse_add_genre_view, name='list'),
        path('verses/new', views.verse_new_story_view, name='new'),
        path('verses/<int:id>', views.verse_detail_view, name='story'),
        path('verses/tree/<int:id>', views.verse_reply_view, name='reply'),
        # profile page
        path('profile/<str:username>', views.user_profile_view, name='profile'),
]

