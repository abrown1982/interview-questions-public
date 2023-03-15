""" Admin for the pets app """
from django.contrib import admin
from .models import Pet


@admin.register(Pet)
class AssignmentAdmin(admin.ModelAdmin):
    """ Admin configuration for the Pet model """
    list_display = ('name', 'animal_type',)
    list_filter = ('animal_type',)


class PetInline(admin.TabularInline):
    """ Inline admin configuration for the Pet model """
    model = Pet
    extra = 0
