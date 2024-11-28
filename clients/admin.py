from django.contrib import admin
from .models import Client, Registration


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'is_member')  # Display these fields in the list view
    search_fields = ('name', 'email', 'phone_number')  # Add search functionality
    list_filter = ('is_member',)  # Add filter options in the sidebar
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone_number', 'address', 'preferred_time', 'is_member')
        }),
    )


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('client', 'class_obj', 'package_type', 'payment_type', 'payment_method', 'price_paid', 'price_left')
    search_fields = ('client__name', 'class_obj__name', 'payment_method')  # Add search functionality
    list_filter = ('payment_type', 'payment_method')  # Add filter options in the sidebar
    fieldsets = (
        (None, {
            'fields': ('client', 'class_obj', 'package_type', 'package', 'payment_type', 'payment_method', 'price_paid', 'price_left', 'classes_attended', 'classes_left')
        }),
    )
