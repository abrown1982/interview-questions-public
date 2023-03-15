""" Views for the Listing app """

from rest_framework import generics

from .models import Listing, Assignment
from .serializers import ListingSerializer, AssignmentSerializer


class ListingList(generics.ListAPIView):
    """
    API View for the Listing.  Has been modified to add the queryset with prefetch_related
    to speed up the data collection for the foreignkey relationships
    """
    serializer_class = ListingSerializer
    queryset = Listing.objects.prefetch_related("pets", "assignments")


class AssignmentCreate(generics.CreateAPIView):
    """
    API View for the Assignment creation.
    """
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
