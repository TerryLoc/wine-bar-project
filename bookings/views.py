from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WineCellar, Booking, UserProfile
from .forms import BookingForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout


class CustomLoginView(LoginView):
    """
    Custom login view to handle user authentication.
    """

    # Specify the template to use for the login page
    template_name = "bookings/login.html"
    # Use the default Django authentication form
    form_class = AuthenticationForm

    # Override the form_valid method to add custom behavior upon successful form submission
    def form_valid(self, form):
        # Get the authenticated user from the form
        user = form.get_user()
        # Log the user in
        auth_login(self.request, user)
        # Display a success message to the user
        messages.success(
            self.request,
            f"Welcome, {user.username} you have successfully logged in! Please enjoy your wine adventure.",
        )
        # Redirect the user to their profile page
        return redirect("bookings:profile")


def wine_list(request):
    """
    Display the list of available wine experiences.
    """
    # Retrieve all wine experiences from the WineCellar model
    wines = WineCellar.objects.all()
    # Render the wine cellar template with the list of wines
    return render(request, "bookings/wine_cellar.html", {"wines": wines})


def register(request):
    """
    Register and handle new users.
    """
    if request.method == "POST":
        # If the request method is POST, create a form instance with the submitted data
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the new user
            user = form.save()
            # Display a success message to the user
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Registration successful! Welcome aboard {user.username}. Please log in to start your wine adventure.",
            )
            # Redirect the user to the login page
            return redirect("bookings:login")
    else:
        # If the request method is GET, create an empty form instance
        form = UserCreationForm()
    # Render the registration template with the form
    return render(request, "bookings/register.html", {"form": form})


@login_required
def book_wine(request, wine_id):
    """
    This view handles the booking of a wine experience.
    """
    # Retrieve the wine experience by its ID, or return a 404 error if not found
    wine = get_object_or_404(WineCellar, id=wine_id)
    if request.method == "POST":
        # If the request method is POST, create a form instance with the submitted data
        form = BookingForm(request.POST)
        if form.is_valid():
            # If the form is valid, create a booking instance without saving to the database yet
            booking = form.save(commit=False)
            # Assign the current user and the selected wine experience to the booking
            booking.user = request.user
            booking.wine_experience = wine
            try:
                # Save the booking to the database
                booking.save()
                # Prepare a success response
                response_data = {
                    "success": True,
                    "message": f"Booking successful! You've reserved {booking.spots_reserved} spot(s) for '{wine.title}'.",
                }
                # Return the success response as JSON
                return JsonResponse(response_data)
            except ValueError as e:
                # Prepare an error response if there is a ValueError
                response_data = {"success": False, "message": str(e)}
                return JsonResponse(response_data)
        else:
            # Prepare an error response if the form is invalid
            response_data = {
                "success": False,
                "message": "Failed to book the experience. Please try again.",
            }
            return JsonResponse(response_data)
    else:
        # If the request method is GET, create an empty form instance
        form = BookingForm()
    # Render the booking form template with the form and the selected wine experience
    return render(request, "bookings/booking_form.html", {"form": form, "wine": wine})


@login_required
def profile(request):
    """
    This view is update to be able to display, update, or delete user profile.
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    bookings = Booking.objects.filter(user=request.user)

    if request.method == "POST":
        if "delete_profile" in request.POST:
            # Handle profile deletion
            user = request.user
            profile.delete()
            user.delete()
            logout(request)
            messages.success(request, "Your profile has been deleted successfully.")
            return redirect("bookings:wine_cellar")  # Redirect to wine cellar page
        else:
            # Handle profile update
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
    """
    Cancel a booking.
    """
    if request.method == "POST":
        try:
            # Retrieve the wine ID and the number of spots to cancel from the POST data
            wine_id = int(request.POST.get("wine_id"))
            spots_to_cancel = int(request.POST.get("spots_to_cancel"))
        except (ValueError, TypeError):
            # Return an error response if the data is invalid
            return JsonResponse({"success": False, "message": "Invalid booking data."})

        # Retrieve the wine experience by its ID, or return a 404 error if not found
        wine = get_object_or_404(WineCellar, id=wine_id)
        # Retrieve the booking for the current user and the selected wine experience
        booking = Booking.objects.filter(
            user=request.user, wine_experience=wine
        ).first()
        if booking:
            if spots_to_cancel >= booking.spots_reserved:
                # If the number of spots to cancel is greater than or equal to the reserved spots, cancel the entire booking
                wine.available_spots += booking.spots_reserved
                wine.save()
                booking.delete()
            else:
                # Otherwise, update the booking with the reduced number of spots
                wine.available_spots += spots_to_cancel
                wine.save()
                booking.spots_reserved -= spots_to_cancel
                booking.save()
            # Return a success response
            return JsonResponse(
                {"success": True, "message": "Booking updated successfully."}
            )
        else:
            # Return an error response if the booking is not found
            return JsonResponse({"success": False, "message": "Booking not found."})
    # Return an error response if the request method is not POST
    return JsonResponse({"success": False, "message": "Invalid request."})
