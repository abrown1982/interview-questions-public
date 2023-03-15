""" url defnitions for the listing app """
from django.urls import path

from .views import ListingList, AssignmentCreate


app_name = 'listings'
urlpatterns = [
    path("", ListingList.as_view(), name="listing"),
    path("assignment/", AssignmentCreate.as_view(), name="assignment")
]
