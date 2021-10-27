from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Review, Ticket, UserFollow
from itertools import chain
from .forms import TicketResponseForm


def index(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    followings = UserFollow.objects.filter(user=request.user)
    for following in followings:
        tickets = tickets | Ticket.objects.filter(user=following.followed_user)
        reviews = reviews | Review.objects.filter(user=following.followed_user)

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


def ticket_response(request):
    if request.method == 'POST' and request.POST.get('headline'):
        form = TicketResponseForm(request.POST)
        if form.is_valid():
            # Create review in database from POST request
            # headline = form.cleaned_data['headline']
            # rating = form.cleaned_data['rating']
            # body = form.cleaned_data['body']
            # ticket = request.POST.get('ticket_id')
            # user = request.user.id
            review = Review(
                headline=form.cleaned_data['headline'],
                rating=form.cleaned_data['rating'],
                body=form.cleaned_data['body'],
                ticket=Ticket.objects.get(pk=request.POST.get('ticket_id')),
                user=request.user
            )
            review.save()

            return HttpResponseRedirect('/reviews/')
    else:
        form = TicketResponseForm()

    ticket = Ticket.objects.get(pk=request.POST.get('ticket_id'))
    context = {
        'ticket': ticket,
        'form': form,
    }
    return render(request, 'reviews/ticket_response.html', context)


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
