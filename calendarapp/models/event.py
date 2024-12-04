from datetime import datetime
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from calendarapp.models import EventAbstract
from accounts.models import User

class StudioLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name
    
class Instructor(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    share_percentage_group = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    share_percentage_private = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)

    def __str__(self):
        return self.name

class PackageType(models.Model):
    name = models.CharField(max_length=100)  
    def __str__(self):
        return self.name
    
class Package(models.Model):
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE, related_name='package_type', null=True, blank=True)
    number_of_sessions = models.PositiveIntegerField()
    member_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])      # Price for members
    non_member_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  # Price for non-members
    
    def __str__(self):
        return f"Package of {self.number_of_sessions} classes"
    
    def get_price(self, is_member):
        return self.member_price if is_member else self.non_member_price

class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self):
        events = Event.objects.filter(is_active=True, is_deleted=False)
        return events

    def get_running_events(self):
        running_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            to_time__gte=datetime.now(), 
            from_time__lte=datetime.now() 
        ).order_by("from_time") 
        return running_events

    # def get_completed_events(self):
    #     completed_events = Event.objects.filter(
    #         is_active=True,
    #         is_deleted=False,
    #         end_time__lt=datetime.now().date(),
    #     )
    #     return completed_events
    
    # def get_upcoming_events(self):
    #     upcoming_events = Event.objects.filter(
    #         is_active=True,
    #         is_deleted=False,
    #         start_time__gt=datetime.now().date(),
    #     )
    #     return upcoming_events

class Event(EventAbstract):
    """Event model representing recurring classes"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    studio_location = models.ForeignKey(StudioLocation, on_delete=models.CASCADE, related_name="events", null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="events", null=True)
    name = models.CharField(max_length=200, null=True)
    days = models.CharField(
        max_length=50,
        null=True,
        help_text="Comma-separated list of days (e.g., Sunday,Tuesday,Friday)",
    )
    from_time = models.TimeField(help_text="Start time for the class (e.g., 13:00)", null=True)
    to_time = models.TimeField(help_text="End time for the class (e.g., 14:00)", null=True)

    objects = EventManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.name} </a>'
