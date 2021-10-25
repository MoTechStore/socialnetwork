from . import views
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from core import views as user_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url




urlpatterns = [

path('', views.index, name='index'),
path('register/', views.registerUser, name='register'),
path('dashboard', views.dashboard, name='dashboard'),
path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
path('feed/',views.feed,name='feed'),
path('followweb/<username>/', views.followweb, name='followweb'),
path('unfollowweb/<username>/', views.unfollowweb, name='unfollowweb'),
path('profile/<username>/', views.profile,name='profile'),
path('postweb/<username>/', views.postweb,name='postweb'),
path('commentweb/<username>/<post_id>/', views.commentweb,name = 'commentweb'),
path('welcome/',views.welcome,name='welcome'),
path('search/', user_views.search, name='search'),







]

