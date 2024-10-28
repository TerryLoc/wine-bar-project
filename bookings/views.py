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


def book_wine(request, wine_id):
    wine = get_object_or_404(wineCellar, id=wine_id)
    # Logic for booking the wine experience can go here
    return render(request, "bookings/booking_success.html", {"wine": wine})


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


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("bookings:wine_cellar")  # Redirect to wine list after login
    else:
        form = AuthenticationForm()
    return render(request, "bookings/login.html", {"form": form})


@login_required
def profile(request):
    # profile = get_object_or_404(UserProfile, user=request.user)

    # create the UserProfile instance if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Check if the delete button was clicked
        if "delete_profile" in request.POST:
            profile.delete()
            messages.success(request, "Profile deleted successfully.")
            return redirect("winery")  # Redirect to homepage after deletion

        # Otherwise, handle form submission for editing
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect(
                "bookings:profile"
            )  # Refresh the profile page to show updated details
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "bookings/profile.html", {"form": form, "profile": profile})
