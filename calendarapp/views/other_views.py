from django.shortcuts import render
from django.views import generic
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from calendarapp.models import  Event
from calendarapp.forms import EventForm
import json
from clients.models import Client, Registration
from calendarapp.models.event import Instructor, ClassOccurrence
from django.utils.timezone import now
import random


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm
  
    def get(self, request, *args, **kwargs):
        
        def generate_bright_color():
            """Generate a random bright color in hex format."""
            r = random.randint(150, 255)  # Red component (bright range)
            g = random.randint(150, 255)  # Green component (bright range)
            b = random.randint(150, 255)  # Blue component (bright range)
            return f"#{r:02x}{g:02x}{b:02x}"  # Convert to hex color code
        
        forms = self.form_class()
        
        clients = Client.objects.all()
        registrations = Registration.objects.all()
        instructors = Instructor.objects.all()
        allevents = Event.objects.all()
   
        occurrences = ClassOccurrence.objects.all()
        event_list = []
        event_colors = {}  # Dictionary to store static colors for each event name

        for occurrence in occurrences:
            event = occurrence.event
            
            if event.name not in event_colors:
                # Assign a bright color to this event name
                event_colors[event.name] = generate_bright_color()
                
        
            filtered_registrations = event.registrations.filter(classes_left__gt=0, expiration_date__gte=now())
            members = event.registrations.values_list('client__name', flat=True)
            members = list(filtered_registrations.values('id', 'client__name', 'classes_left', 'classes_attended'))

            event_list.append({
                "id": occurrence.id,
                "title": event.name,
                "instructor": event.instructor.name,
                "location": event.studio_location.name,
                "start": f"{occurrence.date}T{event.from_time.strftime('%H:%M:%S')}",  # Combine date and time as a string
                "end": f"{occurrence.date}T{event.to_time.strftime('%H:%M:%S')}",      # Combine date and time as a string
                "members": members,
                "backgroundColor": event_colors[event.name],  # Use the bright color
                "borderColor": event_colors[event.name],
                "textColor": "#000000",  # Set text color to black for better contrast
            })

        context = {
            "allevents": allevents.count(),
            "clients": clients.count(),
            "registrations" : registrations.count(),
            "instructors": instructors.count(),
            "form": forms,
            "events": json.dumps(event_list),  # Pass JSON to the frontend
        }
        return render(request, self.template_name, context)

    
    # def post(self, request, *args, **kwargs):
    #     forms = self.form_class(request.POST)
    #     if forms.is_valid():
    #         form = forms.save(commit=False)
    #         form.user = request.user
    #         form.save()
    #         return redirect("calendarapp:calendar")
    #     context = {"form": forms}
    #     return render(request, self.template_name, context)


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def next_week(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=7)
        next.end_time += timedelta(days=7)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_day(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=1)
        next.end_time += timedelta(days=1)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month

