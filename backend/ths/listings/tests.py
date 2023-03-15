from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Listing, Assignment

from datetime import date, timedelta


class ListingList(APITestCase):

    @property
    def listings_url(self):
        """ Shorthand for returning the listings URL through reverse """
        return reverse("listings:listing")

    @property
    def assignment_url(self):
        """ Shorthand for returning the assignment URL through reverse """
        return reverse("listings:assignment")

    def setUp(self):
        """ Setup of the test data """
        self.listing_1 = Listing.objects.create(first_name="Ross", last_name="Geller")
        self.listing_2 = Listing.objects.create(first_name="Phoebe", last_name="Buffay")
        self.assignment_1 = Assignment.objects.create(
            start_date=(date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
            end_date=(date.today() + timedelta(days=8)).strftime("%Y-%m-%d"),
            listing=self.listing_1,
        )
        self.assignment_2 = Assignment.objects.create(
            start_date=(date.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
            end_date=(date.today() + timedelta(days=18)).strftime("%Y-%m-%d"),
            listing=self.listing_2,
        )

    def test_get_200(self):
        """ Checking for a valid response on the listings API """
        response = self.client.get(self.listings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_data(self):
        """ Checking for a valid data response on the listings API """
        response = self.client.get(self.listings_url)
        self.assertEqual(
            response.data['results'],
            [
                {
                    "first_name": self.listing_1.first_name,
                    "last_name": self.listing_1.last_name,
                    "pets": [],
                    "assignments": [self.assignment_1.pk],
                },
                {
                    "first_name": self.listing_2.first_name,
                    "last_name": self.listing_2.last_name,
                    "pets": [],
                    "assignments": [self.assignment_2.pk],
                },
            ],
        )

    def test_assignment_create(self):
        """ Test API endpoint for assignment creation """
        test_data = {
            "start_date": (date.today() + timedelta(days=20)).strftime("%Y-%m-%d"),
            "end_date": (date.today() + timedelta(days=28)).strftime("%Y-%m-%d"),
            "listing": self.listing_1.id
        }

        # Check the reponse code is correct
        response = self.client.post(self.assignment_url, test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the value of the returned data
        response_json = response.json()
        self.assertEqual(response_json["start_date"], test_data["start_date"])
        self.assertEqual(response_json["end_date"], test_data["end_date"])
        self.assertEqual(response_json["listing"], test_data["listing"])

    def test_start_date_later_than_today(self):
        """ Test validation for the start date being later than today """
        test_data = {
            "start_date": (date.today()).strftime("%Y-%m-%d"),
            "end_date": (date.today() + timedelta(days=8)).strftime("%Y-%m-%d"),
            "listing": self.listing_1.id
        }
        # Check the request failed
        response = self.client.post(self.assignment_url, test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the error message
        response_json = response.json()
        self.assertEqual(response_json, {'start_date': ['The start date cannot be earlier than tomorrow']})

    def test_end_date_after_start_date(self):
        """ Test validation for the end date is after the start date """
        test_data = {
            "start_date": (date.today() + timedelta(days=8)).strftime("%Y-%m-%d"),
            "end_date": (date.today() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "listing": self.listing_1.id
        }
        # Check the request failed
        response = self.client.post(self.assignment_url, test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the error message
        response_json = response.json()
        self.assertEqual(response_json, {'end_date': ['End date must be after the start date']})

    def test_date_range_existing(self):
        """ Test validation for there being no overlap with existing assignments for a listing """
        test_data = {
            "start_date": (date.today() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "end_date": (date.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
            "listing": self.listing_1.id
        }

        # Check the request failed
        response = self.client.post(self.assignment_url, test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the error message
        response_json = response.json()
        self.assertEqual(response_json, {'non_field_errors':
                                         ['The assignment cannot overlap with an existing assignment on this listing']})
