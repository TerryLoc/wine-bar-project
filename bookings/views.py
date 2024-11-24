from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import wineCellar, UserProfile, Booking
from .forms import UserProfileForm


# Wine experience views
def wine_list(request):
    """
    Display the list of available wine experiences.
    """
    wines = wineCellar.objects.all()
    return render(request, "bookings/wine_cellar.html", {"wines": wines})


@login_required
def book_wine(request, wine_id):
    """
    Allow authenticated users to book a wine experience.
    """
    wine = get_object_or_404(wineCellar, id=wine_id)

    try:
        # Attempt to create a booking for the user
        booking = Booking.objects.create(
            user=request.user,
            wine_experience=wine,
            spots_reserved=1,  # Reserve 1 spot (can customize for multiple spots)
        )
        messages.success(
            request,
            f"Booking successful! You've reserved 1 spot for '{wine.title}'.",
        )
    except ValueError as e:
        messages.error(request, str(e))

    wines = wineCellar.objects.all()
    return render(
        request,
        "bookings/wine_cellar.html",
        {
            "wines": wines,
            "highlighted_wine": wine,
            "message": messages.get_messages(request),
        },
    )


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
        # Handle profile deletion
        if "delete_profile" in request.POST:
            profile.delete()
            messages.success(request, "Profile deleted successfully.")
            return redirect("winery")

        # Handle booking cancellation
        elif "cancel_booking" in request.POST:
            wine_id = request.POST.get("wine_id")
            try:
                wine = wineCellar.objects.get(id=wine_id)
                booking = Booking.objects.get(user=request.user, wine_experience=wine)
                wine.available_spots += booking.spots_reserved  # Update available spots
                wine.save()
                booking.delete()  # Remove the booking
                messages.success(request, "Booking canceled successfully.")
            except wineCellar.DoesNotExist:
                messages.error(request, "The wine experience does not exist.")
            except Booking.DoesNotExist:
                messages.error(
                    request, "You do not have a booking for this wine experience."
                )
            return redirect("bookings:profile")

        # Handle profile update
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
