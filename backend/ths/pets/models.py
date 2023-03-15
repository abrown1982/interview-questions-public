""" Model definitions for the pets app """
from django.db import models


ANIMAL_TYPE_CHOICES = (
    ("cat", "Cat"),
    ("dog", "Dog"),
    ("fish", "Fish"),
    ("rabbit", "Rabbit"),
)


class Pet(models.Model):
    """ Model definition for the Pet class """
    name = models.CharField(max_length=50)
    animal_type = models.CharField(max_length=10, choices=ANIMAL_TYPE_CHOICES)
    description = models.TextField()
    listing = models.ForeignKey(
        "listings.Listing", on_delete=models.CASCADE, related_name="pets"
    )

    class Meta:
        ordering = ['listing', 'name']

    def __str__(self):
        return f"{self.name} {self.animal_type} on listing {self.listing}"
