from django.urls import path
from . import views

urlpatterns = [
        path('verses', views.verse_list_view, name='list'),
        path('verses/<int:id>', views.verse_detail_view, name='story'),
]

