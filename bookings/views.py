from django.shortcuts import render, get_object_or_404
from .models import wineCellar


def wine_list(request):
    wines = wineCellar.objects.all()
    return render(request, "bookings/wine_cellar.html", {"wines": wines})


def book_wine(request, wine_id):
    # Get the specific wine experience
    wine = get_object_or_404(wineCellar, id=wine_id)

    # Here, you can add booking logic (e.g., reducing available spots, saving booking info)

    return render(
        request, "bookings/booking_success.html", {"wine": wine}
    )  # Create this success template
