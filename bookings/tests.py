from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from bookings.models import UserProfile, Booking, WineCellar
from datetime import date
from decimal import Decimal


class WineCellarModelTest(TestCase):
    def setUp(self):
        # Create a WineCellar instance for testing
        self.wine_cellar = WineCellar.objects.create(
            title="Evening Tasting",
            description="A delightful evening of wine tasting.",
            price=Decimal("50.00"),
            date=date(2025, 5, 1),
            available_spots=10,
            total_spots=20,
            what_to_expect="Expect a variety of reds and whites.",
            join_us_for="Join us for an evening of fun.",
        )

    def test_wine_cellar_creation(self):
        # Test that the WineCellar instance is created correctly
        self.assertEqual(self.wine_cellar.title, "Evening Tasting")
        self.assertEqual(self.wine_cellar.price, Decimal("50.00"))
        self.assertEqual(self.wine_cellar.available_spots, 10)
        self.assertEqual(str(self.wine_cellar), "Evening Tasting")

    def test_has_available_spots(self):
        # Test the has_available_spots method
        self.assertTrue(self.wine_cellar.has_available_spots(5))
        self.assertFalse(self.wine_cellar.has_available_spots(15))


class UserProfileModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
        )

    def test_user_profile_creation(self):
        # Test that a UserProfile is created automatically via signal
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, "testuser")
        self.assertEqual(profile.name, "Test User")
        self.assertEqual(profile.email, "testuser@example.com")  # Should now pass
        self.assertEqual(str(profile), "testuser")

    def test_user_profile_save(self):
        # Test the save method updates the name field
        profile = UserProfile.objects.get(user=self.user)
        self.user.first_name = "Updated"
        self.user.last_name = "Name"
        self.user.save()
        profile.refresh_from_db()
        self.assertEqual(profile.name, "Updated Name")


class BookingModelTest(TestCase):
    def setUp(self):
        # Create a test user and wine cellar
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.wine_cellar = WineCellar.objects.create(
            title="Evening Tasting",
            description="A delightful evening of wine tasting.",
            price=Decimal("50.00"),
            date=date(2025, 5, 1),
            available_spots=10,
            total_spots=20,
            what_to_expect="Expect a variety of reds and whites.",
            join_us_for="Join us for an evening of fun.",
        )

    def test_booking_creation(self):
        # Test creating a booking and updating available spots
        booking = Booking.objects.create(
            user=self.user, wine_experience=self.wine_cellar, spots_reserved=3
        )
        self.wine_cellar.refresh_from_db()
        self.assertEqual(booking.spots_reserved, 3)
        self.assertEqual(self.wine_cellar.available_spots, 7)  # 10 - 3
        self.assertEqual(str(booking), "Booking by testuser for Evening Tasting")

    def test_booking_no_spots_available(self):
        # Test booking fails if not enough spots are available
        with self.assertRaises(ValueError):
            Booking.objects.create(
                user=self.user,
                wine_experience=self.wine_cellar,
                spots_reserved=15,  # More than available_spots (10)
            )


class ProfileViewTest(TestCase):
    def setUp(self):
        # Create a test user (this triggers the signal to create a UserProfile)
        self.user = User.objects.create_user(
            username="testuser", password="testpass", email="testuser@example.com"
        )
        # Retrieve the existing UserProfile created by the signal
        self.profile = UserProfile.objects.get(user=self.user)
        # Update the profile with test data
        self.profile.contact_number = "0871234567"
        self.profile.email = "testuser@example.com"
        self.profile.save()
        self.client.login(username="testuser", password="testpass")

    def test_profile_page_loads(self):
        response = self.client.get(reverse("bookings:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/profile.html")

    def test_profile_update(self):
        data = {
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated@example.com",
            "contact_number": "0879876543",
        }
        response = self.client.post(reverse("bookings:profile"), data)
        self.assertRedirects(response, reverse("bookings:profile"))
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.profile.contact_number, "0879876543")

    def test_profile_deletion(self):
        response = self.client.post(reverse("bookings:profile"), {"delete_profile": ""})
        self.assertRedirects(response, reverse("bookings:wine_cellar"))
        self.assertFalse(User.objects.filter(username="testuser").exists())
        self.assertFalse(
            UserProfile.objects.filter(email="testuser@example.com").exists()
        )
