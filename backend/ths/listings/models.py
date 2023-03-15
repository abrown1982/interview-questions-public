""" Model definitions for the listings app """
from django.db import models
from django.core.exceptions import ValidationError


class Listing(models.Model):
    """ Model definition for the Listing class """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        ordering = ['id',]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Assignment(models.Model):
    """ Model definition for the Assignment class """
    start_date = models.DateField()
    end_date = models.DateField()
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        help_text="The listing that this assignment relates to",
        related_name="assignments",
    )

    class Meta:
        ordering = ['start_date', 'end_date']

    def __str__(self):
        return f"{self.start_date} {self.end_date} on listing {self.listing}"

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be later than start date")
