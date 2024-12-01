from django import forms
from .models import UserProfile
from .models import Booking
from django.core.exceptions import ValidationError
import re  # For regex validation


#  Form for user profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["name", "email", "contact_number"]

    # Form fields with custom validation
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your name", "required": "required"}
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email", "required": "required"}
        ),
    )
    contact_number = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your contact number",
                "pattern": "^\+?[0-9\s-]{7,15}$",
                "required": "required",
            }
        ),
    )

    # Clean name field to ensure it only contains letters and spaces
    def clean_name(self):
        name = self.cleaned_data.get("name")  # Get name
        if not name:
            raise ValidationError("Name is required.")
        if not re.match(r"^[A-Za-z\s]+$", name):
            raise ValidationError("Name must contain only letters and spaces.")
        return name

    # Clean email field to ensure it is a valid email address
    def clean_email(self):
        email = self.cleaned_data.get("email")  # Get email
        if not email:
            raise ValidationError("Email is required.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Basic email regex
            raise ValidationError("Enter a valid email address.")
        return email

    # Clean contact number field to ensure it only contains numbers, spaces, or dashes
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get("contact_number")  # Get contact number
        if not contact_number:
            raise ValidationError("Contact number is required.")
        if not re.match(
            r"^\+?[0-9\s-]{7,15}$", contact_number
        ):  # Allows +, numbers, spaces, dashes
            raise ValidationError(
                "Contact number must contain only numbers, spaces, or dashes, and be 7-15 characters long."
            )
        return contact_number


# Form for booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["spots_reserved"]
        widgets = {
            "spots_reserved": forms.NumberInput(attrs={"min": 1}),
        }
