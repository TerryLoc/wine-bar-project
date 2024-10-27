from django.db import models


class wineCellar(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    available_spots = models.PositiveIntegerField()
    what_to_expect = models.TextField()  # New field for 'What to Expect'
    join_us_for = models.TextField()  # New field for 'Join Us'

    def __str__(self):
        return self.title  # Use title instead of name
