from django.shortcuts import render
# from django.http import HttpResponse
from .models import Review, Ticket, UserFollow
from django.contrib.auth.models import User
from itertools import chain


def index(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    followings = UserFollow.objects.filter(user=request.user)
    for following in followings:
        tickets | Ticket.objects.filter(user=following.followed_user)
        reviews | Review.objects.filter(user=following.followed_user)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda x: x.time_created, reverse=True)[:10]
    context = {
        'tickets_and_reviews': tickets_and_reviews
    }
    return render(request, 'reviews/index.html', context)


def my_posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda x: x.time_created, reverse=True)
    context = {
        'tickets_and_reviews': tickets_and_reviews
    }
    return render(request, 'reviews/my_posts.html', context)


def ticket_creation(request):
    context = {}
    return render(request, 'reviews/ticket_creation', context)


def review_creation(request):
    ticket = Ticket.objects.get(pk=request.POST.get('ticket_id'))
    context = {
        'ticket': ticket,
    }
    return render(request, 'reviews/review_creation.html', context)


def user_follows(request):
    followings = UserFollow.objects.filter(user=request.user)
    followed_bys = UserFollow.objects.filter(followed_user=request.user)
    if not followings:
        followings = ["Vous n'avez pas encore d'abonnements"]
    if not followed_bys:
        followed_bys = ["Personne ne s'est encore abonné"]
    context = {
        'followings': followings,
        'followed_bys': followed_bys
    }
    return render(request, 'reviews/user_follows.html', context)
