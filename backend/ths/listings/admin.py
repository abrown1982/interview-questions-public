""" Admin file for the listings app """
from django.contrib import admin

from .models import Listing, Assignment
from pets.admin import PetInline


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """ Admin configuration for the Assignment model """
    list_display = ('start_date', 'end_date', 'listing')
    date_hierarchy = 'start_date'
    search_fields = ['listing__first_name', 'listing__last_name']


class AssignmentInline(admin.TabularInline):
    """ Inline admin configuration for the Assignment model """
    model = Assignment
    extra = 0


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """ Admin configuration for the Listing model """
    list_display = ('first_name', 'last_name')
    search_fields = ['first_name', 'last_name']
    inlines = [AssignmentInline, PetInline]
