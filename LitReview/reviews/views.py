from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Review, Ticket, UserFollow
from itertools import chain
from .forms import TicketResponseForm, TicketCreationForm, ReviewCreationForm, UserSearchForm
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login


def redirect_to_reviews_index(request):
    response = redirect('reviews:index')
    return response


@login_required(login_url='reviews:login')
def index(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    followings = UserFollow.objects.filter(user=request.user)
    for following in followings:
        tickets = tickets | Ticket.objects.filter(user=following.followed_user)
        reviews = reviews | Review.objects.filter(user=following.followed_user)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda x: x.time_created, reverse=True)
    context = {
        'tickets_and_reviews': tickets_and_reviews
    }
    return render(request, 'reviews/index.html', context)


@login_required(login_url='reviews:login')
def my_posts(request):
    if request.method == 'POST':
        if request.POST.get('role') == 'delete':
            if request.POST.get('review_id'):
                get_object_or_404(Review, pk=request.POST.get('review_id')).delete()
            elif request.POST.get('ticket_id'):
                get_object_or_404(Ticket, pk=request.POST.get('ticket_id')).delete()

        elif request.POST.get('role') == 'modify':
            # checking 'review_id' presence first to recognize if it is a review,
            # because both reviews and tickets POSTs returns a 'ticket_id' attribute
            if request.POST.get('review_id'):
                review = get_object_or_404(Review, pk=request.POST.get('review_id'))
                ticket = get_object_or_404(Ticket, pk=request.POST.get('ticket_id'))
                data = {
                    'headline': review.headline,
                    'rating': review.rating,
                    'body': review.body
                }
                form = TicketResponseForm(initial=data)
                context = {
                    'review': review,
                    'ticket': ticket,
                    'form': form,
                }
                return render(request, 'reviews/ticket_response.html', context)

            elif request.POST.get('ticket_id'):
                ticket = get_object_or_404(Ticket, pk=request.POST.get('ticket_id'))
                data = {
                    'title': ticket.title,
                    'description': ticket.description,
                    'image': ticket.image
                }
                form = TicketCreationForm(initial=data)
                context = {
                    'form': form,
                    'ticket': ticket
                }
                return render(request, 'reviews/ticket_creation.html', context)

    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda x: x.time_created, reverse=True)
    context = {
        'tickets_and_reviews': tickets_and_reviews
    }
    return render(request, 'reviews/my_posts.html', context)


class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('reviews:my_posts')


@login_required(login_url='reviews:login')
def ticket_creation(request):
    if request.method == 'POST':
        form = TicketCreationForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('ticket_id'):
                ticket = get_object_or_404(Ticket, pk=request.POST.get('ticket_id'))
                ticket.title = form.cleaned_data['title']
                ticket.description = form.cleaned_data['description']
                ticket.image = form.cleaned_data['image']
                ticket.save()
                return HttpResponseRedirect('/reviews/my_posts')
            else:
                ticket = Ticket(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    image=form.cleaned_data['image'],
                    user=request.user
                )
                ticket.save()
                return HttpResponseRedirect('/reviews/')
    else:
        form = TicketCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'reviews/ticket_creation.html', context)


@login_required(login_url='reviews:login')
def ticket_response(request):
    # if request.method == 'POST' and request.POST.get('headline'): (old condition, don't know why anymore...)
    # try:
    if request.method == 'POST':
        form = TicketResponseForm(request.POST)
        if form.is_valid():
            if request.POST.get('review_id'):
                review = get_object_or_404(Review, pk=request.POST.get('review_id'))
                review.headline = form.cleaned_data['headline']
                review.rating = form.cleaned_data['rating']
                review.body = form.cleaned_data['body']
                review.save()
                return HttpResponseRedirect('/reviews/my_posts')
            else:
                review = Review(
                    headline=form.cleaned_data['headline'],
                    rating=form.cleaned_data['rating'],
                    body=form.cleaned_data['body'],
                    ticket=get_object_or_404(Ticket, pk=request.POST.get('ticket_id')),
                    user=request.user
                )
                review.save()
                return HttpResponseRedirect('/reviews/')
    else:
        form = TicketResponseForm()

    ticket = get_object_or_404(Ticket, pk=request.POST.get('ticket_id'))
    context = {
        'ticket': ticket,
        'form': form,
    }
    return render(request, 'reviews/ticket_response.html', context)
    # except:
    #     return HttpResponseRedirect('/reviews/')


@login_required(login_url='reviews:login')
def review_creation(request):
    if request.method == 'POST':
        form = ReviewCreationForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = Ticket(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data.get('image'),
                user=request.user
            )
            ticket.save()

            review = Review(
                headline=form.cleaned_data['headline'],
                rating=form.cleaned_data['rating'],
                body=form.cleaned_data['body'],
                ticket=ticket,
                user=request.user
            )
            review.save()

            return HttpResponseRedirect('/reviews/')
    else:
        form = ReviewCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'reviews/review_creation.html', context)


@login_required(login_url='reviews:login')
def user_follows(request):
    form = UserSearchForm()
    search_matches = []
    search_message = ''
    if request.method == 'POST':
        if request.POST.get('role') == 'search':
            form = UserSearchForm(request.POST)
            if form.is_valid():
                username_searched = form.cleaned_data['username_searched']
                if User.objects.filter(username=username_searched):
                    user_to_follow = get_object_or_404(User, username=username_searched)
                    if user_to_follow == request.user:
                        search_message = f"Vous ne pouvez pas vous abonner à vous-même !"
                    elif UserFollow.objects.filter(user=request.user, followed_user=user_to_follow):
                        search_message = f"Vous êtes déjà abonnée à {user_to_follow}"
                    else:
                        new_follow = UserFollow(user=request.user, followed_user=user_to_follow)
                        new_follow.save()
                        search_message = f"Vous êtes maintenant abonné à {user_to_follow}"
                else:
                    search_matches = User.objects.filter(username__icontains=username_searched)  #  exclude request.user
                    if not search_matches:
                        search_message = "Aucun utilisateur ne correspond à cette recherche"

        elif request.POST.get('role') == 'search_all':
            unwanted = User.objects.filter(followed_by__user=request.user) | User.objects.filter(pk=request.user.pk)
            search_matches = User.objects.exclude(pk__in=[user.pk for user in unwanted])
            if not search_matches:
                if len(unwanted) == 1:
                    search_message = "Vous êtes le seul utilisateur de LITReview !"
                else:
                    search_message = "Vous êtes déjà abonné a tous les utilisateurs"
        elif request.POST.get('role') == 'delete':
            following_id = request.POST.get('following_id')
            follow_to_delete = get_object_or_404(UserFollow, pk=following_id)
            user_to_unfollow = follow_to_delete.followed_user.username
            follow_to_delete.delete()
            search_message = f"{ user_to_unfollow } ne fait plus partie de votre liste d'abonnements"
        elif request.POST.get('role') == 'add':
            user_to_follow = get_object_or_404(User, pk=request.POST.get('user_to_follow_id'))
            new_follow = UserFollow(user=request.user, followed_user=user_to_follow)
            new_follow.save()
            search_message = f"Vous êtes maintenant abonné à {user_to_follow}"

    followings = UserFollow.objects.filter(user=request.user)
    followed_bys = UserFollow.objects.filter(followed_user=request.user)
    followed_users = []
    for following in followings:
        followed_users.append(following.followed_user)
    context = {
        'form': form,
        'followings': followings,
        'followed_bys': followed_bys,
        'followed_users': followed_users,
        'search_matches': search_matches,
        'search_message': search_message
    }
    return render(request, 'reviews/user_follows.html', context)


def user_creation(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/reviews/')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)
