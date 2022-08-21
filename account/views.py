import json

from actions.models import Action
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .forms import LoginForm, ProfileEditForm, UserEditForm, UserRegisterForm
from .models import Contact, Profile


class HomeView(TemplateView):
    template_name = "account/home.html"


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/account/dashboard/")

                else:
                    return HttpResponse("Disabled Account")

            else:
                return HttpResponse("Invalid Login Curd")

    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})


class UserLogout(LoginRequiredMixin, LogoutView):
    template_name = "account/logout.html"


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)[:10]
    return render(
        request, "account/dashboard.html", {"section": "dashboard", "actions": actions}
    )


def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegisterForm()

    return render(request, "account/register.html", {"user_form": user_form})


def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, "saved change successfully", extra_tags="alert-success"
            )
        else:
            messages.error(request, "invalid data", extra_tags="alert-danger")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        "account/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True).exclude(id=request.user.id)
    return render(request, "account/user/list.html", {"users": users})


@login_required
def user_detail(request, username):
    user_object = get_object_or_404(User, username=username, is_active=True)
    return render(request, "account/user/detail.html", {"user_object": user_object})


@login_required
@require_POST
def user_follow(request):
    data = json.loads(request.body)
    user_id = data.get("user_id")
    action = data.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status": "ok"})

        except:
            pass

    return JsonResponse({"status": "error"})
