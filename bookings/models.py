from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# This model represents a wine cellar experience that users can book. It includes the title, description, price, date, available spots, total spots, what to expect, and join us for fields.
class WineCellar(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    available_spots = models.PositiveIntegerField()
    total_spots = models.PositiveIntegerField()
    what_to_expect = models.TextField()
    join_us_for = models.TextField()

    # This method returns the title of the wine cellar experience.
    def __str__(self):
        return self.title

    # This method checks if there are available spots for the given number of spots.
    def has_available_spots(self, num_spots=1):
        return self.available_spots >= num_spots


# This model represents a user profile that is linked to the User model. It includes the user, name, email, and contact number fields.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    # This method saves the user profile and concatenates the first and last name from the user profile.
    def save(self, *args, **kwargs):
        # Concatenate first and last name from the user profile
        self.name = f"{self.user.first_name} {self.user.last_name}"
        super(UserProfile, self).save(*args, **kwargs)

    # This method returns the username of the user.
    def __str__(self):
        return self.user.username


# This signal creates a user profile when a new user is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # when a User is created with an email, the UserProfile will inherit it.
        UserProfile.objects.get_or_create(
            user=instance, defaults={"email": instance.email}  # Set email from User
        )


# This signal saves the user profile when the user is saved.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()


# Here the Booking model is created with the user, wine experience, spots reserved, and timestamp fields. The save method is overridden to check if there are enough available spots for the booking.
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    wine_experience = models.ForeignKey(
        WineCellar, on_delete=models.CASCADE, related_name="bookings"
    )
    spots_reserved = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    # This method returns the booking details.
    def __str__(self):
        return f"Booking by {self.user.username} for {self.wine_experience.title}"

    # This method checks if there are enough available spots for the booking and updates the available spots accordingly.
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.wine_experience.has_available_spots(self.spots_reserved):
                self.wine_experience.available_spots -= self.spots_reserved
                self.wine_experience.save()
            else:
                raise ValueError("Not enough spots available for this experience.")
        super().save(*args, **kwargs)
