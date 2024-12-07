from django import forms
from .models import UserProfile
from .models import Booking
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
import re  # For regex validation


#  Form for user profile
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z\s]+$",
                message="First name must contain only letters and spaces.",
            )
        ],
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z\s]+$",
                message="Last name must contain only letters and spaces.",
            )
        ],
    )
    email = forms.EmailField(
        max_length=200,
        required=True,
        validators=[EmailValidator(message="Enter a valid email address.")],
    )
    contact_number = forms.CharField(
        max_length=15,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^\+?[0-9\s-]{7,15}$",
                message="Contact number must contain only numbers, spaces, or dashes.",
            )
        ],
    )

    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "email", "contact_number"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise ValidationError("First name is required.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError("Last name is required.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email is required.")
        return email

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get("contact_number")
        if not contact_number:
            raise ValidationError("Contact number is required.")
        return contact_number


# Form for booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["spots_reserved"]
        widgets = {
            "spots_reserved": forms.NumberInput(attrs={"min": 1}),
        }
