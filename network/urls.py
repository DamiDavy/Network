from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('user/<int:num>/', views.person, name='person'),
    path('follow/<int:fel>/<int:fol>', views.follow, name='follow'),
    path('following/<int:num>/', views.following, name='following'),
    path('edit/<int:num>/<int:fel>/', views.edit, name='edit'),

        # API Routes
    path("post", views.compose, name="compose"),
    path("like/<int:n>", views.like, name="like"),
]
