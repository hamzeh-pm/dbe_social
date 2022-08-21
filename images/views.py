import json

from actions.utils import create_action
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from utils.redis import RedisClient

from .forms import ImageCreateForm
from .models import Image

# Create your views here.


@login_required
def image_create(request):
    if request.method == "POST":
        image_form = ImageCreateForm(request.POST)
        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.user = request.user
            image.save()
            create_action(request.user, "bookmark a image", image)
            messages.success(
                request, "saved change successfully", extra_tags="alert-success"
            )
        else:
            messages.error(request, "error in saving image", extra_tags="alert-danger")

    else:
        image_form = ImageCreateForm()

    return render(request, "images/create.html", {"image_form": image_form})


class ImageListView(LoginRequiredMixin, ListView):
    model = Image
    template_name = "images/list.html"
    context_object_name = "images"


class ImageDetailView(LoginRequiredMixin, DetailView):
    model = Image
    template_name = "images/detail.html"

    def get_context_data(self, **kwargs):
        image = kwargs.get("object")
        rc = RedisClient()
        total_view = rc.redis_client.incr(f"image:{image.id}:views")
        print(total_view)
        return super().get_context_data(**kwargs)


@login_required
@require_POST
def image_like(request):
    data = json.loads(request.body)
    image_id = data.get("image_id")
    action = data.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.user_likes.add(request.user)
            else:
                result = image.user_likes.remove(request.user)
            return JsonResponse({"status": "ok"})

        except:
            pass

    return JsonResponse({"status": "error"})
