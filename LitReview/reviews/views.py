from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from itertools import chain

from .forms import TicketResponseForm, TicketCreationForm, ReviewCreationForm, UserSearchForm
from .models import Review, Ticket, UserFollow


def redirect_to_reviews_index(request):
    """
    Simple view used in urls.py to redirect from root to reviews app index.
    :param request:
    :return: Redirection to reviews' index.
    """
    return redirect('reviews:index')


@login_required(login_url='reviews:login')
def index(request):
    """
    This index view finds tickets and reviews from followed users and actual users.
    Merges them and sort them the most recent first.
    :param request:
    :return: A render of the index page using it's template.
    """
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    followings = UserFollow.objects.filter(user=request.user)
    for following in followings:
        tickets = tickets | Ticket.objects.filter(user=following.followed_user)
        reviews = reviews | Review.objects.filter(user=following.followed_user)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda x: x.time_created, reverse=True)
    star_count = [0, 1, 2, 3, 4]
    context = {
        'tickets_and_reviews': tickets_and_reviews,
        'star_count': star_count
    }
    return render(request, 'reviews/index.html', context)


@login_required(login_url='reviews:login')
def my_posts(request):
    """
    This index view finds tickets and reviews from actual users.
    Merges them and sort them the most recent first.
    It also handles deletion and modification of tickets and reviews.
    :param request:
    :return: A render of the index page using it's template.
    """
    star_count = [0, 1, 2, 3, 4]
    if request.method == 'POST':
        if request.POST.get('role') == 'delete':
            if request.POST.get('review_id'):
                return redirect(f"/reviews/delete_review/{request.POST.get('review_id')}")
            elif request.POST.get('ticket_id'):
                return redirect(f"/reviews/delete_ticket/{request.POST.get('ticket_id')}")

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
                    'role': 'modify',
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
                    'ticket': ticket,
                }
                return render(request, 'reviews/ticket_creation.html', context)

    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda x: x.time_created, reverse=True)
    context = {
        'tickets_and_reviews': tickets_and_reviews,
        'star_count': star_count
    }
    return render(request, 'reviews/my_posts.html', context)


@login_required(login_url='reviews:login')
def ticket_creation(request):
    """
    View to modify or create a new ticket.
    :param request:
    :return: A redirection to my_posts if the ticket is modified,
        a redirection to feed page if the ticket is created,
        or a render of it's template with a blank form if user wants to create a new ticket.
    """
    if request.method == 'POST':
        form = TicketCreationForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('ticket_id'):
                ticket = get_object_or_404(Ticket, pk=request.POST.get('ticket_id'))
                ticket.title = form.cleaned_data['title']
                ticket.description = form.cleaned_data['description']
                ticket.image = form.cleaned_data['image']
                ticket.save()
                messages.success(request, f'Votre ticket "{ticket.title}" a bien été modifié.')
                return redirect('/reviews/my_posts')
            else:
                ticket = Ticket(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    image=form.cleaned_data['image'],
                    user=request.user
                )
                ticket.save()
                messages.success(request, f'Votre ticket "{ticket.title}" a bien été créé.')
                return redirect('/reviews/')
    else:
        form = TicketCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'reviews/ticket_creation.html', context)


@login_required(login_url='reviews:login')
def ticket_response(request):
    """
    View to modify or create a review in response to an existing ticket.
    :param request:
    :return: A redirection to my_posts if the review is modified,
        a redirection to feed page if the review is created,
        or a render of it's template with a blank form if user wants to create a new review.
    """
    if request.method == 'POST':
        form = TicketResponseForm(request.POST)
        if form.is_valid():
            if request.POST.get('review_id'):
                review = get_object_or_404(Review, pk=request.POST.get('review_id'))
                review.headline = form.cleaned_data['headline']
                review.rating = form.cleaned_data['rating']
                review.body = form.cleaned_data['body']
                review.save()
                messages.success(request, f'Votre critique "{review.headline}" a bien été modifiée.')
                return redirect('/reviews/my_posts')
            else:
                review = Review(
                    headline=form.cleaned_data['headline'],
                    rating=form.cleaned_data['rating'],
                    body=form.cleaned_data['body'],
                    ticket=get_object_or_404(Ticket, pk=request.POST.get('ticket_id')),
                    user=request.user
                )
                review.save()
                messages.success(request, f'Votre critique "{review.headline}" a bien été créée.')
                return redirect('/reviews/')
    else:
        form = TicketResponseForm()

    ticket = get_object_or_404(Ticket, pk=request.POST.get('ticket_id'))
    context = {
        'ticket': ticket,
        'form': form,
    }
    return render(request, 'reviews/ticket_response.html', context)


@login_required(login_url='reviews:login')
def review_creation(request):
    """
    View to create a ticket and it's review at the same time.
    :param request:
    :return: A redirection to feed page if the ticket and review is created,
        or a render of it's template with a blank form if user wants to create a new ticket and review.
    """
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

            messages.success(request, f'Votre critique "{review.headline}" a bien été créée.')
            return redirect('/reviews/')
    else:
        form = ReviewCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'reviews/review_creation.html', context)


@login_required(login_url='reviews:login')
def user_follows(request):
    """
    View to show user's follows and followers, to search and add new follows, or to delete existing follows.
    :param request:
    :return: A render of it's template with the search, add or delete form, or a blank form.
    """
    form = UserSearchForm()
    search_matches = []
    if request.method == 'POST':
        if request.POST.get('role') == 'search':
            form = UserSearchForm(request.POST)
            if form.is_valid():
                username_searched = form.cleaned_data['username_searched']
                if User.objects.filter(username=username_searched):
                    user_to_follow = get_object_or_404(User, username=username_searched)
                    if user_to_follow == request.user:
                        messages.success(request, f"Vous ne pouvez pas vous abonner à vous-même !")
                    elif UserFollow.objects.filter(user=request.user, followed_user=user_to_follow):
                        messages.success(request, f"Vous êtes déjà abonnée à {user_to_follow}.")
                    else:
                        new_follow = UserFollow(user=request.user, followed_user=user_to_follow)
                        new_follow.save()
                        messages.success(request, f"Vous êtes maintenant abonné à {user_to_follow}.")
                else:
                    search_matches = User.objects.filter(
                        username__icontains=username_searched).exclude(
                        pk=request.user.pk)
                    if not search_matches:
                        messages.success(request, "Aucun utilisateur ne correspond à cette recherche.")

        elif request.POST.get('role') == 'search_all':
            search_matches = User.objects.exclude(followed_by__user=request.user).exclude(pk=request.user.pk)
            if not search_matches:
                if len(User.objects.all()) == 1:
                    messages.success(request, "Vous êtes le seul utilisateur de LITReview !")
                else:
                    messages.success(request, "Vous êtes déjà abonné a tous les utilisateurs.")

        elif request.POST.get('role') == 'delete':
            following_id = request.POST.get('following_id')
            return redirect(f"/reviews/delete_follow/{following_id}")
        elif request.POST.get('role') == 'add':
            user_to_follow = get_object_or_404(User, pk=request.POST.get('user_to_follow_id'))
            new_follow = UserFollow(user=request.user, followed_user=user_to_follow)
            new_follow.save()
            messages.success(request, f"Vous êtes maintenant abonné à {user_to_follow}.")

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
    }
    return render(request, 'reviews/user_follows.html', context)


def user_creation(request):
    """
    This view manages user creation using generic django UserCreationForm.
    All passwords filters have been deactivated in settings.py.
    :param request:
    :return: A render of it's template with UserCreationForm as a context,
        or a redirection to the feed page after automatically logging the user if the user creation is successful.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/reviews/')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


class TicketDeleteView(DeleteView):
    """
    Ticket delete confirmation view, children of django's generic DeleteView.
    """
    model = Ticket
    success_url = reverse_lazy('reviews:my_posts')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(TicketDeleteView, self).get_object()
        if obj.user == self.request.user:
            return obj
        else:
            raise PermissionDenied

    def delete(self, request, *args, **kwargs):
        """ Hook to add a confirmation message to the messages queue when ticket is deleted """
        obj = self.get_object()
        messages.success(self.request, f'Votre ticket "{obj.title}" a bien été supprimé.')
        return super(TicketDeleteView, self).delete(request, *args, **kwargs)


class ReviewDeleteView(DeleteView):
    """
    Review delete confirmation view, children of django's generic DeleteView.
    """
    model = Review
    success_url = reverse_lazy('reviews:my_posts')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(ReviewDeleteView, self).get_object()
        if obj.user == self.request.user:
            return obj
        else:
            raise PermissionDenied

    def delete(self, request, *args, **kwargs):
        """ Hook to add a confirmation message to the messages queue when ticket is deleted """
        obj = self.get_object()
        messages.success(self.request, f'Votre critique "{obj.headline}" a bien été supprimée.')
        return super(ReviewDeleteView, self).delete(request, *args, **kwargs)


class UserFollowDeleteView(DeleteView):
    """
    User's Follow delete confirmation view, children of django's generic DeleteView.
    """
    model = UserFollow
    success_url = reverse_lazy('reviews:user_follows')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(UserFollowDeleteView, self).get_object()
        if obj.user == self.request.user:
            return obj
        else:
            raise PermissionDenied

    def delete(self, request, *args, **kwargs):
        """ Hook to add a confirmation message to the messages queue when ticket is deleted """
        obj = self.get_object()
        messages.success(self.request, f"{obj.followed_user} ne fait plus partie de votre liste d'abonnements.")
        return super(UserFollowDeleteView, self).delete(request, *args, **kwargs)
