from django.shortcuts import render, redirect
from django.views import generic
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from calendarapp.models import  Event
from calendarapp.forms import EventForm
import json
from clients.models import Client, Registration
from calendarapp.models.event import Instructor

class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        # statistical numbers
         
        clients = Client.objects.all()
        registrations = Registration.objects.all()
        instructors = Instructor.objects.all()
        allevents = Event.objects.all()
        events = Event.objects.get_all_events()
        events_month = Event.objects.get_running_events()
        event_list = []

        # Map day names to their corresponding weekday numbers
        day_mapping = {
            "Sunday": 6,
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
        }

        # Define the date range to generate events for (e.g., next 4 weeks)
        today = datetime.today()
        end_date = today + timedelta(weeks=4)

        for event in events:
            # Convert `event.days` (e.g., "['Sunday', 'Wednesday']") to a Python list
            days = eval(event.days)  # Ensure `event.days` is stored as a stringified list
            for day in days:
                # Find the next occurrence of the day within the range
                current_date = today
                while current_date <= end_date:
                    if current_date.weekday() == day_mapping[day]:
                        # Add the event for this date
                        filtered_registrations = event.registrations.filter(classes_left__gt=0)
                        # members = event.registrations.values_list('client__name', flat=True)
                        members = list(filtered_registrations.values('id', 'client__name', 'classes_left', 'classes_attended'))
                        event_list.append({
                            "id": event.id,
                            "title": event.name,
                            "instructor": event.instructor.name,
                            "location": event.studio_location.name,
                            "days":event.days,
                            "start": f"{current_date.strftime('%Y-%m-%d')}T{event.from_time.strftime('%H:%M:%S')}",
                            "end": f"{current_date.strftime('%Y-%m-%d')}T{event.to_time.strftime('%H:%M:%S')}",
                            "members": members, 
                        })
                    # Increment the date
                    current_date += timedelta(days=1)

        context = {
            "allevents": allevents.count(),
            "clients": clients.count(),
            "registrations" : registrations.count(),
            "instructors": instructors.count(),
            "form": forms,
            "events": json.dumps(event_list),  # Pass JSON to the frontend
            "events_month": events_month,
        }
        return render(request, self.template_name, context)
   

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)


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

