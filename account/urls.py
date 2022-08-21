from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.UserLogout.as_view(), name="user_logout"),
    path("dashboard/", views.dashboard, name="user_dashboard"),
    path("register/", views.register, name="user_register"),
    path("profile/", views.edit, name="user_profile"),
    path("users/", views.user_list, name="user_list"),
    path("users/<str:username>/", views.user_detail, name="user_detail"),
    path("follow/", views.user_follow, name="user_follow"),
]
