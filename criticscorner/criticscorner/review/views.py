from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Reviewer


def index(request):
    return HttpResponse("Pagina de entrada da app review.")


def registar_user(request):
    if request.method == "POST":
        username = request.POST.get('user')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username, email=email, password=password)
        rv = Reviewer(user=user)
        rv.save()

        return HttpResponseRedirect(reverse('review:loginview'))
    else:
        return render(request, 'review/registaruser.html')


def loginview(request):
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('review:index'))
        else:
            return render(request, 'review/login.html', {'error_message': "Utilizador ou palavra passe inválidas!"}, )
    else:
        return render(request, 'review/login.html')


@login_required(login_url='review:loginview')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('review:index'))
