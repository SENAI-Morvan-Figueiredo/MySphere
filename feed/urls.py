from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('post/<int:post_id>/share/', views.share_post, name='share_post'),
    path('hashtag/<str:tag>/', views.hashtag_view, name='hashtag'),
    path('search/', views.search_view, name='search'),
    path('autocomplete/', views.autocomplete_view, name='autocomplete'),
]
