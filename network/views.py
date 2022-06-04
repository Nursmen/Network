import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import *

def index(request, page=1):
    p = Paginator(Post.objects.all().order_by('-created_at'), 10)
    return render(request, "network/index.html", {'pages': p, 'page': page})

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

def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        author = request.user
        post = Post(content=content, author=author)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html")

def get_json_posts(request, page=1):
    posts = Post.objects.all().order_by('-created_at')
    p = Paginator(posts, 10)
    return JsonResponse(list(p.page(page).object_list.values()), safe=False)

def get_json_users(request):
    users = User.objects.all()
    return JsonResponse(list(users.values()), safe=False)

def user_page(request, username, page=1):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')

    p = Paginator(posts, 10)

    return render(request, "network/user_page.html", {
        "profile": user,
        "posts": posts,
        "pages": p,
        'page': page
    })

def follow(request, username):
    user = User.objects.get(username=username)
    request.user.following.add(user)    
    # add one to the number of followers
    user.subscribers += 1
    user.save()
    return HttpResponseRedirect(reverse("user_page", args=[username]))

def unfollow(request, username):
    user = User.objects.get(username=username)
    request.user.following.remove(user)
    # subtract one from the number of followers
    user.subscribers -= 1
    user.save()
    return HttpResponseRedirect(reverse("user_page", args=[username]))

def follow_page(request):
    return render(request, "network/follow_page.html")

def following(request, username):
    user = User.objects.get(username=username)
    following = user.following.all()
    posts = Post.objects.filter(author__in=following).order_by('-created_at')
    return JsonResponse(list(posts.values()), safe=False)

@csrf_exempt
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        post.content = data['content']
        post.save()

    return HttpResponse(status=204)