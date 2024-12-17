from django.views.generic import ListView
from django.shortcuts import render, redirect

from calendarapp.models import Event
from calendarapp.forms import EventForm

from datetime import datetime, timedelta
from calendarapp.models.event import ClassOccurrence
import ast  

class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/events_list.html"
    model = Event
    context_object_name = "events" 
    form_class = EventForm

    def get_queryset(self):
        return Event.objects.get_all_events()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.user = request.user
            new_event.save()
            self.populate_class_occurrences(new_event)
            
            return redirect("calendarapp:all_events")  
      
        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)
    
    def populate_class_occurrences(self, event):
        # today = datetime.today()
        # first_day_of_month = today.replace(day=1)
        # last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        start_date = event.start_duration
        end_date = event.end_duration

        # Parse the days from the event
        days = ast.literal_eval(event.days)  # Convert stringified list to Python list

        # Iterate through the days in the current month
        current_date = start_date
        while current_date <= end_date:
            if current_date.strftime("%A") in days:
                # Create a ClassOccurrence if it doesn't exist
                ClassOccurrence.objects.get_or_create(
                    event=event,
                    date=current_date,
                )
            current_date += timedelta(days=1)

        print("Class occurrences for the event have been generated.")

# class AllEventsListView(ListView):
#     """ All event list views """

#     template_name = "calendarapp/events_list.html"
#     model = Event
#     form_class = EventForm

#     def get_queryset(self, request, *args, **kwargs):
#         forms = self.form_class()
#         events = Event.objects.get_all_events()
#         context = {
#             "form": forms,
#             "events": events, 
#         }
#         return render(request, self.template_name, context)

      
    
#     def post(self, request, *args, **kwargs):
#         forms = self.form_class(request.POST)
#         if forms.is_valid():
#             form = forms.save(commit=False)
#             form.user = request.user
#             form.save()
#             return redirect("calendarapp:all_events")
#         context = {"form": forms}
#         return render(request, self.template_name, context)




# class RunningEventsListView(ListView):
#     """ Running events list view """

#     template_name = "calendarapp/events_list.html"
#     model = Event

#     def get_queryset(self):
#         return Event.objects.get_running_events()

# class UpcomingEventsListView(ListView):
#     """ Upcoming events list view """

#     template_name = "calendarapp/events_list.html"
#     model = Event

#     def get_queryset(self):
#         return Event.objects.get_upcoming_events()
    
# class CompletedEventsListView(ListView):
#     """ Completed events list view """

#     template_name = "calendarapp/events_list.html"
#     model = Event

#     def get_queryset(self):
#         return Event.objects.get_completed_events()
    


