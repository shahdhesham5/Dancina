from django.shortcuts import render, redirect
from django.views import generic
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from calendarapp.models import  Event
from calendarapp.models.event import StudioLocation, Instructor
from calendarapp.forms import EventForm
import json
from clients.models import Client, Registration
from calendarapp.models.event import Instructor, ClassOccurrence
from django.utils.timezone import now
import random
from django.db.models import Q
from django.contrib import messages
from calendarapp.forms import AddOccurrenceClassForm
from accounts.decorators import allowed_users

from calendarapp.forms import AddPrivateClass, AddOtherClass
import ast  

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

        # Assign static colors to events
        for event in allevents:
            if not event.color:  # Only assign a color if it doesn't already have one
                event.color = generate_bright_color()
                event.save()  # Save the color to the database

        for occurrence in occurrences:
            event = occurrence.event

            # Filter registrations based on classes_left and expiration_date
            filtered_registrations = event.registrations.filter(classes_left__gt=0, expiration_date__gte=now())

            # Exclude members who have already attended the class on the specific date
            members = list(filtered_registrations.exclude(
                Q(client__attendances__attendance_date=occurrence.date)
            ).values('id', 'client__name', 'classes_left', 'classes_attended'))

        # Check if the event is private
            if event.is_private:
                if occurrence.from_time and occurrence.to_time:
                    start_time = f"T{occurrence.from_time.strftime('%H:%M:%S')}"
                    end_time = f"T{occurrence.to_time.strftime('%H:%M:%S')}"
                else:
                    start_time = f"T{event.from_time.strftime('%H:%M:%S')}"
                    end_time = f"T{event.to_time.strftime('%H:%M:%S')}"
            else:
                    start_time = f"T{event.from_time.strftime('%H:%M:%S')}"
                    end_time = f"T{event.to_time.strftime('%H:%M:%S')}"
                    
            event_list.append({
                "id": occurrence.id,
                "title": event.name,
                "instructor": event.instructor.name,
                "location": event.studio_location.name,
                "start": f"{occurrence.date}{start_time}",  # Combine date and time as a string
                "end": f"{occurrence.date}{end_time}",    
                "members": members,
                "is_private": event.is_private,
                "is_other": event.is_other,
                "backgroundColor": event.color,  # Use the static color from the database
                "borderColor": event.color,
                "textColor": "#000000",  # Set text color to black for better contrast
            })

        context = {
            "allevents": allevents.count(),
            "clients": clients.count(),
            "registrations": registrations.count(),
            "instructors": instructors.count(),
            "form": forms,
            "events": json.dumps(event_list),  # Pass JSON to the frontend
        }
        return render(request, self.template_name, context)


def add_private_class(request):
    if request.method == 'POST':
        form = AddPrivateClass(request.POST)
        if form.is_valid():
            # Save the private class instance
            private_class = form.save(commit=False)
            
            # Get the first studio location if not provided in the form
            if not private_class.studio_location:
                # Fetch the first studio location from the database
                default_studio_location = StudioLocation.objects.first()

                # If there is no studio location in the database, handle the case gracefully
                if not default_studio_location:
                    return JsonResponse({'status': 'error', 'message': 'No default studio location available'})

                private_class.studio_location = default_studio_location

            

            # Now create the event for the private class
            event = Event.objects.create(
                user=request.user,  # Assign the logged-in user
                name=private_class.name,
                instructor = private_class.instructor,
                from_time=form.cleaned_data['from_time'],
                to_time=form.cleaned_data['to_time'],
                start_duration=private_class.start_duration,
                end_duration=private_class.start_duration,  # Assuming the private class is only for one day
                is_private = True,
                studio_location=private_class.studio_location,
            )

            # Create a ClassOccurrence for the private class (this will be shown on the calendar)
            ClassOccurrence.objects.create(
                event=event,
                date=private_class.start_duration
            )
            return redirect('calendarapp:calendar')
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is not valid'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def add_other_class(request):
    if request.method == 'POST':
        form = AddOtherClass(request.POST)
        if form.is_valid():
            # Save the private class instance
            other_class = form.save(commit=False)
        
            if not other_class.instructor:
                default_instructor = Instructor.objects.first()
                if not default_instructor:
                    return JsonResponse({'status': 'error', 'message': 'No default instructor available'})

                other_class.instructor = default_instructor


            # Now create the event for the private class
            event = Event.objects.create(
                user=request.user,  # Assign the logged-in user
                name=other_class.name,
                instructor = other_class.instructor,
                days=form.cleaned_data['days'],
                studio_location=other_class.studio_location,
                from_time=form.cleaned_data['from_time'],
                to_time=form.cleaned_data['to_time'],
                start_duration=other_class.start_duration,
                end_duration=other_class.end_duration,  # Assuming the private class is only for one day
                is_other = True,
            )

            # Create a ClassOccurrence for the private class (this will be shown on the calendar)
            populate_class_occurrences(event)
            
            return redirect('calendarapp:calendar')
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is not valid'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def add_new_session(request):
    if request.method == "POST":
        form = AddOccurrenceClassForm(request.POST)
        if form.is_valid():
            # Retrieve the event_id from the form
            event_id = request.POST.get('event_id')
            event = Event.objects.get(id=event_id)
            
            # Create the ClassOccurrence with the associated event
            ClassOccurrence.objects.create(
                event=event,
                date=form.cleaned_data['date'],
                from_time=form.cleaned_data['from_time'],
                to_time=form.cleaned_data['to_time'],
            )
            
            return redirect("calendarapp:calendar")
    
    # If the form is not valid, render the same page again with the form
    context = {"form": form}
    return render(request, 'private_classess.html', context)


def delete_class_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Class deleted successfully.')
        return redirect('calendarapp:all_events')

def delete_event(request, event_id):
    event = get_object_or_404(ClassOccurrence, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def delete_private_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Class deleted successfully.')
        return redirect('calendarapp:get_private_classes')


def get_private_classes(request):
    events = Event.objects.filter(is_active=True, is_private=True) 
    others = Event.objects.filter(is_active=True, is_private=False, is_other=True) 
    context = {"events": events, "others": others}
    return render(request, 'private_classess.html', context)


# def edit_event(request, event_id):
#     event = get_object_or_404(Event, pk=event_id)

#     if request.method == 'POST':
#         form = EventForm(request.POST, instance=event) 
#         if form.is_valid():
#             form.save()
#             return redirect('calendarapp:all_events')
#     else:
#         form = EventForm(instance=event)

#     return render(request, 'edit_event.html', {'form': form, 'event': event})
@allowed_users(groups=['Dancina SuperAdmin'])
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    old_days = event.days  # Store the original days for comparison

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event) 
        if form.is_valid():
            updated_event = form.save(commit=False)  # Don't save to DB yet to avoid overwriting
            new_days = form.cleaned_data.get('days')
            
            # Save the form instance
            updated_event.save()

            # Check if the 'days' field has changed
            if new_days != old_days:
                # Clear existing occurrences for this event
                ClassOccurrence.objects.filter(event=updated_event).delete()

                # Repopulate occurrences
                populate_class_occurrences(updated_event)

            return redirect('calendarapp:all_events')
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form, 'event': event})

def populate_class_occurrences(event):
    start_date = event.start_duration
    end_date = event.end_duration

    # Parse the days from the event
    days = ast.literal_eval(event.days)  # Convert stringified list to Python list

    # Iterate through the days in the specified date range
    current_date = start_date
    while current_date <= end_date:
        if current_date.strftime("%A") in days:
            # Create a ClassOccurrence if it doesn't exist
            ClassOccurrence.objects.get_or_create(
                event=event,
                date=current_date,
            )
        current_date += timedelta(days=1)

    print("Class occurrences for the event have been regenerated.")

@allowed_users(groups=['Dancina SuperAdmin'])
def edit_private_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = AddPrivateClass(request.POST, instance=event) 
        if form.is_valid():
            form.save()
            return redirect('calendarapp:get_private_classes')
    else:
        form = AddPrivateClass(instance=event)

    return render(request, 'edit_private_event.html', {'form': form, 'event': event})

@allowed_users(groups=['Dancina SuperAdmin'])
def edit_other_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = AddOtherClass(request.POST, instance=event) 
        if form.is_valid():
            form.save()
            return redirect('calendarapp:get_private_classes')
    else:
        form = AddOtherClass(instance=event)

    return render(request, 'edit_other_event.html', {'form': form, 'event': event})


def populate_class_occurrences(event):
    start_date = event.start_duration
    end_date = event.end_duration

    # Parse the days from the event
    if event.days:
        days = event.days
    if not days:
        print(f"Event ID {event.id} has no valid days specified.")

    # Iterate through the days in the current month
    current_date = start_date
    while current_date <= end_date:
        if current_date.strftime("%A") in days:
            # Create a ClassOccurrence if it doesn't exist
            ClassOccurrence.objects.create(
                event=event,
                date=current_date,
            )
        current_date += timedelta(days=1)

    print("Class occurrences for the event have been generated.")







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

