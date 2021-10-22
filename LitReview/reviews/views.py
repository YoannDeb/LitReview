from django.shortcuts import render
# from django.http import HttpResponse
from .models import Review, Ticket


def index(request):
    tickets = Ticket.objects.all().order_by('-time_created')
    context = {
        'tickets': tickets
    }
    return render(request, 'reviews/index.html', context)
