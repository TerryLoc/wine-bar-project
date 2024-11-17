from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import wineCellar
from .models import UserProfile
from .forms import UserProfileForm


# Wine experience views
def wine_list(request):
    wines = wineCellar.objects.all()
    return render(request, "bookings/wine_cellar.html", {"wines": wines})


@login_required
def book_wine(request, wine_id):
    wine = get_object_or_404(wineCellar, id=wine_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if wine.book_spot(user_profile):
        messages.success(request, "Booking successful! You've reserved a spot.")
    else:
        messages.error(request, "Sorry, no spots are available for this experience.")

    return redirect("bookings:wine_cellar")  # Redirect back to wine cellar page


# User authentication views
def register(request):
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
    bookings = profile.bookings.all()

    if request.method == "POST":
        if "delete_profile" in request.POST:
            profile.delete()
            messages.success(request, "Profile deleted successfully.")
            return redirect("winery")

        elif "cancel_booking" in request.POST:
            wine_id = request.POST.get("wine_id")
            wine = get_object_or_404(wineCellar, id=wine_id)
            profile.bookings.remove(wine)  # Remove booking from profile
            wine.available_spots += 1  # Increment available spots
            wine.save()
            messages.success(request, "Booking canceled successfully.")
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
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(
                "bookings:wine_cellar/profile"
            )  # Redirect to profile after login
    else:
        form = AuthenticationForm()
    return render(request, "bookings/login.html", {"form": form})
