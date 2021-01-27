from django.urls import path, include
from .views import ListPostsAPI, ViewPostAPI

app_name = 'api'



urlpatterns = [
    path('posts/', ListPostsAPI.as_view(), name='api_for_all_posts'),
    path('posts/<int:pk>', ViewPostAPI.as_view(), name='api_for_single_post'),

]