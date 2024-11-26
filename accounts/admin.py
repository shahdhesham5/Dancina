from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'is_staff', 'is_active')


class UserAdmin(BaseUserAdmin):
    # Use custom forms for creating and changing users
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # Fields to display in the admin panel
    list_display = ('email', 'is_staff', 'is_active', 'date_joined', 'last_updated')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    # Configure the fields for changing an existing user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active')}),
        (_('Important dates'), {'fields': ()}),  # Exclude non-editable fields here
    )

    # Configure the fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    # Read-only fields (like date_joined) that should be displayed but not edited
    readonly_fields = ('date_joined', 'last_updated')


# Register the custom UserAdmin to handle our custom user model
admin.site.register(User, UserAdmin)
