from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [

    path('', views.controller, name='controller'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('login_from_navbar/', views.user_login, name='login_from_navbar'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/draft/', views.published_or_draft, name='draft'),
    path('profile/published/', views.published_or_draft, name='published'),

]