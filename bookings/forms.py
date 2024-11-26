from django import forms
from .models import UserProfile
from .models import Booking


#  Form for user profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["name", "email", "contact_number"]


# Form for booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["spots_reserved"]
        widgets = {
            "spots_reserved": forms.NumberInput(attrs={"min": 1}),
        }
