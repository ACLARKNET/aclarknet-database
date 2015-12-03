from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .forms import ClientForm
from .models import Client

# Create your views here.


def about(request):
    return render(request, 'about.html', {})


def client(request, pk):
    context = {}
    client = get_object_or_404(Client, pk=pk)
    context['client'] = client
    return render(request, 'client.html', context)


def client_edit(request, pk=None):
    context = {}

    if pk is None:
        form = ClientForm()
    else:
        client = get_object_or_404(Client, pk=pk)
        form = ClientForm(instance=client)

    context['form'] = form
    return render(request, 'client_edit.html', context)


def contact(request):
    return render(request, 'contact.html', {})


def home(request):
    context = {}
    clients = Client.objects.all()
    context['clients'] = clients
    return render(request, 'home.html', context)
