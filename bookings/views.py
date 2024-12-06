from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import wineCellar, Booking, UserProfile
from .forms import BookingForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm


def wine_list(request):
    """
    Display the list of available wine experiences.
    """
    wines = wineCellar.objects.all()
    return render(request, "bookings/wine_cellar.html", {"wines": wines})


@login_required
def book_wine(request, wine_id):
    wine = get_object_or_404(wineCellar, id=wine_id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.wine_experience = wine
            try:
                booking.save()
                messages.success(
                    request,
                    f"Booking successful! You've reserved {booking.spots_reserved} spot(s) for '{wine.title}'.",
                )
            except ValueError as e:
                messages.error(request, str(e))
            return redirect("bookings:profile")
        else:
            messages.error(request, "Failed to book the experience. Please try again.")
    else:
        form = BookingForm()
    return render(request, "bookings/booking_form.html", {"form": form, "wine": wine})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}.")
            return redirect("bookings:login")
    else:
        form = UserCreationForm()
    return render(request, "bookings/register.html", {"form": form})


@login_required
def profile(request):
    """
    Display and manage user profile.
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    bookings = Booking.objects.filter(user=request.user)

    if request.method == "POST":
        if "delete_profile" in request.POST:
            profile.delete()
            messages.success(request, "Profile deleted.")
            return redirect("winery")
        elif "cancel_booking" in request.POST:
            try:
                wine_id = int(request.POST.get("wine_id"))
                spots_to_cancel = int(request.POST.get("spots_to_cancel", 0))
            except (ValueError, TypeError):
                messages.error(request, "Invalid booking data.")
                return redirect("bookings:profile")

            wine = get_object_or_404(wineCellar, id=wine_id)
            booking = Booking.objects.filter(
                user=request.user, wine_experience=wine
            ).first()
            if booking:
                if (
                    spots_to_cancel >= booking.spots_reserved
                    or "cancel_all" in request.POST
                ):
                    wine.available_spots += booking.spots_reserved
                    wine.save()
                    booking.delete()
                else:
                    wine.available_spots += spots_to_cancel
                    wine.save()
                    booking.spots_reserved -= spots_to_cancel
                    booking.save()
                messages.success(request, "Booking updated successfully.")
            else:
                messages.error(request, "Booking not found.")
            return redirect("bookings:profile")
        else:
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("bookings:profile")
            else:
                messages.error(request, "Failed to update profile. Please try again.")
    else:
        form = UserProfileForm(instance=profile)

    return render(
        request, "bookings/profile.html", {"form": form, "bookings": bookings}
    )
