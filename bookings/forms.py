# Description: This file contains the form for user profile and booking.
from .models import Booking
from django import forms
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator


# Form for user profile
class UserProfileForm(forms.ModelForm):
    # Field for first name with validation to ensure it contains only letters and spaces
    first_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z\s]+$",
                message="First name must contain only letters and spaces.",
            )
        ],
    )
    # Field for last name with validation to ensure it contains only letters and spaces
    last_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z\s]+$",
                message="Last name must contain only letters and spaces.",
            )
        ],
    )
    # Field for email with validation to ensure it is a valid email address
    email = forms.EmailField(
        max_length=100,
        required=True,
        validators=[EmailValidator(message="Enter a valid email address.")],
    )
    # Field for contact number with validation to ensure it contains only numbers, spaces, or dashes
    contact_number = forms.CharField(
        min_length=7,
        max_length=15,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^\+?[0-9\s-]{7,15}$",
                message="Contact number must contain only numbers, spaces, or dashes.",
            )
        ],
    )

    # Meta class to specify the model and fields for the form
    class Meta:
        model = UserProfile
        # Fields to include in the form
        fields = ["first_name", "last_name", "email", "contact_number"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            # Initialize the form fields with the user's existing data
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name

    def clean_first_name(self):
        # Custom validation for the first name field
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise ValidationError("First name is required.")
        return first_name

    def clean_last_name(self):
        # Custom validation for the last name field
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError("Last name is required.")
        return last_name

    def clean_email(self):
        # Custom validation for the email field
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email is required.")
        return email

    def clean_contact_number(self):
        # Custom validation for the contact number field
        contact_number = self.cleaned_data.get("contact_number")
        if not contact_number:
            raise ValidationError("Contact number is required.")
        return contact_number


# Form for booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["spots_reserved"]
        # Widget to ensure the spots_reserved field is a number input with a minimum value of 1
        widgets = {
            "spots_reserved": forms.NumberInput(attrs={"min": 1}),
        }
