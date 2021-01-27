from django.urls import path
from . import views

app_name = 'civilopedia'

urlpatterns = [
    path('controller/', views.controller, name='controller'),
    path('posts/', views.ListPosts.as_view(), name='posts'),
    path('posts/<slug:tag>', views.ListPostsByTagOrCategory.as_view(), name='posts_by_tag'),
    path('posts/<slug:category>', views.ListPostsByTagOrCategory.as_view(), name='posts_by_category'),
    path('posts/search/', views.ListPostsBySearch.as_view(), name='posts_by_search'),
    path('tags/', views.tags_page, name='tags_page'),
    path('add-post/', views.CreatePost.as_view(), name='add_post'),
    path('add-tags/', views.AddTags.as_view(), name='add_tags'),
    path('change-post/<slug:slug>', views.ChangePost.as_view(), name='change_post'),
    path('view-post/<slug:slug>', views.ViewPost.as_view(), name='view_post'),
    path('get-token/', views.get_token, name='get_token'),

]

# posts_by_search