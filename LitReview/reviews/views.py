from django.shortcuts import render
# from django.http import HttpResponse
from .models import Review, Ticket, UserFollow
from django.contrib.auth.models import User


def index(request):
    tickets = Ticket.objects.all().order_by('-time_created')
    context = {
        'tickets': tickets
    }
    return render(request, 'reviews/index.html', context)


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
