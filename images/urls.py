from django.urls import path

from . import views

app_name = "images"

urlpatterns = [
    path("create/", views.image_create, name="create"),
    path("gallery/", views.ImageListView.as_view(), name="gallery"),
    path("gallery/<slug:slug>/", views.ImageDetailView.as_view(), name="image_detail"),
    path("like/", views.image_like, name="image_like"),
]
