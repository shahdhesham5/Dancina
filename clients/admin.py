from django.contrib import admin
from .models import Client, Registration
# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'is_member')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('is_member',)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('client', 'class_obj', 'package', 'payment_type', 'price_paid', 'price_left', 'classes_attended', 'classes_left')
    list_filter = ('payment_type', 'class_obj', 'client')
    search_fields = ('client__name', 'class_obj__name')