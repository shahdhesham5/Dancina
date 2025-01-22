from django import template

register = template.Library()

@register.filter
def is_superAdmin(user):
    """Check if the user belongs to a specific group."""
    if user.is_authenticated:
        return user.groups.filter(name='Dancina SuperAdmin').exists()
    return False
