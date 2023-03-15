""" Serialisers for the listing app """
from django.db.models import Q

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Listing, Assignment

from datetime import date


class ListingSerializer(serializers.ModelSerializer):
    """ Serialiser for the Listing model """

    class Meta:
        model = Listing
        fields = ["first_name", "last_name", "pets", "assignments"]


class AssignmentSerializer(serializers.ModelSerializer):
    """ Serialiser for the Assignment model """

    class Meta:
        model = Assignment
        fields = ["id", "start_date", "end_date", "listing"]

    def validate(self, data):
        # Check the start date is later than today
        self.start_date_later_than_today(data["start_date"])

        # Check the end date is after the start date
        self.end_date_after_start_date(data["start_date"], data["end_date"])

        # Check there is no overlap with existing assignments for this listing
        self.date_range_existing(data["start_date"], data["end_date"], data["listing"])

        # Continue to the automated ModelZerializer validation
        return super().validate(data)

    def start_date_later_than_today(self, start_date):
        """ Check the start date is later than today """
        if date.today() >= start_date:
            raise serializers.ValidationError({"start_date": "The start date cannot be earlier than tomorrow"})

    def end_date_after_start_date(self, start_date, end_date):
        """ Check the end date is after the start date """
        if end_date <= start_date:
            raise ValidationError({"end_date": "End date must be after the start date"})

    def date_range_existing(self, new_start_date, new_end_date, listing):
        """ Check there is no overlap with existing assignments for this listing """
        # Find any assignments where the new_start_date or new_end_date is between the start_date and end_date.
        num_assignments = Assignment.objects.filter(listing=listing).filter(
            Q(start_date__lte=new_start_date) & Q(end_date__gt=new_start_date)
            or
            Q(start_date__lt=new_end_date) & Q(end_date__gte=new_start_date)
        ).count()
        if num_assignments > 0:
            raise ValidationError("The assignment cannot overlap with an existing assignment on this listing")
