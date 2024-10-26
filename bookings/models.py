from django.db import models


class wineCellar(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    available_spots = models.PositiveIntegerField()

    def __str__(self):
        return self.title  # Corrected to return the title field
