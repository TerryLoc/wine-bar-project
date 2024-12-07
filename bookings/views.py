from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import wineCellar, Booking, UserProfile
from .forms import BookingForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse


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
                response_data = {
                    "success": True,
                    "message": f"Booking successful! You've reserved {booking.spots_reserved} spot(s) for '{wine.title}'.",
                }
                return JsonResponse(response_data)
            except ValueError as e:
                response_data = {"success": False, "message": str(e)}
                return JsonResponse(response_data)
        else:
            response_data = {
                "success": False,
                "message": "Failed to book the experience. Please try again.",
            }
            return JsonResponse(response_data)
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
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user.first_name = form.cleaned_data["first_name"]
            profile.user.last_name = form.cleaned_data["last_name"]
            profile.user.email = profile.email
            profile.user.save()
            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("bookings:profile")
        else:
            messages.error(request, "Failed to update profile. Please try again.")
    else:
        form = UserProfileForm(instance=profile)

    return render(
        request, "bookings/profile.html", {"form": form, "bookings": bookings}
    )


@login_required
def cancel_booking(request):
    if request.method == "POST":
        try:
            wine_id = int(request.POST.get("wine_id"))
            spots_to_cancel = int(request.POST.get("spots_to_cancel"))
        except (ValueError, TypeError):
            return JsonResponse({"success": False, "message": "Invalid booking data."})

        wine = get_object_or_404(wineCellar, id=wine_id)
        booking = Booking.objects.filter(
            user=request.user, wine_experience=wine
        ).first()
        if booking:
            if spots_to_cancel >= booking.spots_reserved:
                wine.available_spots += booking.spots_reserved
                wine.save()
                booking.delete()
            else:
                wine.available_spots += spots_to_cancel
                wine.save()
                booking.spots_reserved -= spots_to_cancel
                booking.save()
            return JsonResponse(
                {"success": True, "message": "Booking updated successfully."}
            )
        else:
            return JsonResponse({"success": False, "message": "Booking not found."})
    return JsonResponse({"success": False, "message": "Invalid request."})
