from django.shortcuts import render
from .models import wineCellar


def wine_list(request):
    wines = wineCellar.objects.all()
    return render(request, "bookings/wine_cellar.html", {"wines": wines})
