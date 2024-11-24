from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Wine cellar model (unchanged except for removing `book_spot`)
class wineCellar(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    available_spots = models.PositiveIntegerField()
    total_spots = models.PositiveIntegerField()
    what_to_expect = models.TextField()
    join_us_for = models.TextField()

    def __str__(self):
        return self.title

    # Optional utility to check if spots are available
    def has_available_spots(self, num_spots=1):
        return self.available_spots >= num_spots


# User profile model (adjusted to remove the ManyToMany with wineCellar)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username


# New Booking model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    wine_experience = models.ForeignKey(
        wineCellar, on_delete=models.CASCADE, related_name="bookings"
    )
    spots_reserved = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)  # When the booking was made

    def __str__(self):
        return f"Booking by {self.user.username} for {self.wine_experience.title}"

    # Override save to reduce available spots when a booking is created
    def save(self, *args, **kwargs):
        if not self.pk:  # Only reduce spots if this is a new booking
            if self.wine_experience.has_available_spots(self.spots_reserved):
                self.wine_experience.available_spots -= self.spots_reserved
                self.wine_experience.save()
            else:
                raise ValueError("Not enough spots available for this experience.")
        super().save(*args, **kwargs)


# Signals to manage UserProfile creation/saving
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()
