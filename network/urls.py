
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<int:page>/', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('new_post', views.new_post, name='new_post'),
    path('get_posts/<int:page>', views.get_json_posts, name='get_posts'),
    path('get_users', views.get_json_users, name='get_users'),

    path('users/<str:username>/<int:page>', views.user_page, name='user_page'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),

    path('follow_page', views.follow_page, name='follow_page'),
    path('following/<str:username>', views.following, name='following'),

    path('edit/<int:post_id>', views.edit_post, name='edit_post'),
]
