from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User, Post


class PostListView(generic.ListView):
    model = Post
    paginate_by = 10

def person(request, num):
    person = User.objects.get(pk=num)
    post_list = person.post_set.all()

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/person.html", {
                    "person": person,
                    "page_obj": page_obj,
                    "page_number": page_number
                    })

@login_required
def follow(request, fel, fol):
    fella = User.objects.get(pk=fel)
    follower = User.objects.get(pk=fol)
    if follower in fella.followers.all():
        fella.followers.remove(follower)
    else:
        fella.followers.add(follower)
    return HttpResponseRedirect(reverse("person", args=(fel,)))

@csrf_exempt
@login_required
def edit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        num = data.get("id")
        content = data.get("text")
        post = Post.objects.get(pk=num)
        post.content = content
        post.save()
        return JsonResponse(post.serialize(), status=204)
    else:
        return JsonResponse({"message": "Method Not Allowed"}, status=405)

@login_required
def following(request, num):
    person = User.objects.get(pk=num)
    following = person.following.all()
    posts = Post.objects.filter(user__in=following).order_by('-timestamp')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
                    "posts": posts,
                    "page_obj": page_obj,
                    "page_number": page_number
                    })

# @csrf_exempt
@login_required
def compose(request):
    if request.method == "POST":
        content = request.POST["post"]
        user = request.user
        post = Post(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return JsonResponse({"message": "Method Not Allowed"}, status=405)

@csrf_exempt
@login_required
def like(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        num = data.get("id")
        post = Post.objects.get(pk=num)

        person = User.objects.get(username=request.user.username)

        if person in post.likes.all():
            post.likes.remove(person)
            post.save()
            return JsonResponse(data={"message": "Like is removed"}, status=204)
        else:
            post.likes.add(person)
            post.save()
            return JsonResponse(data={"message": "Like is added"}, status=200)
    else:
        return JsonResponse({"message": "Method Not Allowed"}, status=405)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
