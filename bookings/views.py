from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import wineCellar, UserProfile, Booking
from .forms import UserProfileForm
from .forms import BookingForm


# Wine experience views
def wine_list(request):
    """
    Display the list of available wine experiences.
    """
    wines = wineCellar.objects.all()
    return render(request, "bookings/wine_cellar.html", {"wines": wines})


login_required


def book_wine(request, wine_id):
    """
    Allow authenticated users to book a wine experience.
    """
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
            return redirect("bookings:wine_cellar")
    else:
        form = BookingForm()
    return render(request, "bookings/profile.html", {"form": form, "wine": wine})


# User authentication views
def register(request):
    """
    Register a new user.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("bookings:login")  # Redirect to login after registration
    else:
        form = UserCreationForm()
    return render(request, "bookings/register.html", {"form": form})


@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    bookings = Booking.objects.filter(user=request.user)

    if request.method == "POST":
        if "delete_profile" in request.POST:
            profile.delete()
            messages.success(request, "Profile deleted successfully.")
            return redirect("winery")

        elif "cancel_booking" in request.POST:
            wine_id = request.POST.get("wine_id")
            spots_to_cancel = int(request.POST.get("spots_to_cancel", 0))

            wine = get_object_or_404(wineCellar, id=wine_id)
            user_booking = Booking.objects.filter(
                user=request.user, wine_experience=wine
            ).first()

            if user_booking:
                # If cancelling all spots
                if (
                    spots_to_cancel >= user_booking.spots_reserved
                    or "cancel_all" in request.POST
                ):
                    wine.available_spots += user_booking.spots_reserved
                    wine.save()
                    user_booking.delete()
                    messages.success(request, "Booking canceled successfully.")
                else:
                    # Cancel only the requested number of spots
                    wine.available_spots += spots_to_cancel
                    wine.save()
                    user_booking.spots_reserved -= spots_to_cancel
                    user_booking.save()
                    messages.success(
                        request,
                        f"{spots_to_cancel} spot(s) have been canceled successfully.",
                    )
            else:
                messages.error(request, "No booking found to cancel.")
            return redirect("bookings:profile")

        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("bookings:profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(
        request,
        "bookings/profile.html",
        {
            "form": form,
            "profile": profile,
            "bookings": bookings,
        },
    )


# Login view with authentication
def login_view(request):
    """
    Handle user login functionality.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("bookings:profile")  # Redirect to profile after login
    else:
        form = AuthenticationForm()
    return render(request, "bookings/login.html", {"form": form})
