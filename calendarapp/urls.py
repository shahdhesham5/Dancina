from django.urls import path

from . import views
from .views.views import get_instructors, add_instructor, get_studios, add_studio, get_packages, add_package

app_name = "calendarapp"

urlpatterns = [
    path("calender/", views.CalendarViewNew.as_view(), name="calendar"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),


    # path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    # path("event/<int:event_id>/details/", views.event_details, name="event-detail"),

    # path(
    #     "event/<int:pk>/remove",
    #     views.EventMemberDeleteView.as_view(),
    #     name="remove_event",
    # ),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    # path(
    #     "running-event-list/",
    #     views.RunningEventsListView.as_view(),
    #     name="running_events",
    # ),
    # path(
    #     "upcoming-event-list/",
    #     views.UpcomingEventsListView.as_view(),
    #     name="upcoming_events",
    # ),
    # path(
    #     "completed-event-list/",
    #     views.CompletedEventsListView.as_view(),
    #     name="completed_events",
    # ),
    path("instructors/",get_instructors,name="instructors"),
    path("add_instructor/",add_instructor,name="add_instructor"),
    path("studios/",get_studios,name="studios"),
    path("add_studio/",add_studio,name="add_studio"),
    path("packages/",get_packages,name="packages"),
    path('add_package/',add_package, name='add_package'),
]
