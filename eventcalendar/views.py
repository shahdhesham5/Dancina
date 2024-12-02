from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# from calendarapp.models import Event
# from clients.models import Client, Registration
# from calendarapp.models.event import Instructor

class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"

    def get(self, request, *args, **kwargs):
        # events = Event.objects.get_all_events()
        # clients = Client.objects.all()
        # registrations = Registration.objects.all()
        # instructors = Instructor.objects.all()
        # running_events = Event.objects.get_running_events()
        # completed_events = Event.objects.get_completed_events()
        # upcoming_events = Event.objects.get_upcoming_events()
        # context = {
        #     "events": events.count(),
        #     "clients": clients.count(),
        #     "registrations" : registrations.count(),
        #     "instructors": instructors.count(),
        #     "running_events": running_events,
        #     "completed_events": completed_events.count(),
        #     "upcoming_events": upcoming_events
        # }
        return render(request, self.template_name)
