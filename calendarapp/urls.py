from django.urls import path

from . import views
from .views.views import get_instructors, add_instructor, get_studios, add_studio, get_packages, add_package, edit_instructor, delete_instructor,delete_studio, edit_studio, delete_package_type,delete_package
from . views.other_views import add_private_class, add_other_class, edit_event, delete_class_event, get_private_classes, add_new_session,edit_private_event, edit_other_event, delete_private_event
app_name = "calendarapp"

urlpatterns = [
    path("calender/", views.CalendarViewNew.as_view(), name="calendar"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('edit_event/<int:event_id>/', edit_event, name='edit_event'),
    path('edit_private_event/<int:event_id>/', edit_private_event, name='edit_private_event'),
    path('edit_other_event/<int:event_id>/', edit_other_event, name='edit_other_event'),
    path('delete_class_event/<int:event_id>/', delete_class_event, name='delete_class_event'),
    path('delete_private_event/<int:event_id>/', delete_private_event, name='delete_private_event'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path('add_private_class/',add_private_class, name='add_private_class'),
    path('add_other_class/',add_other_class, name='add_other_class'),
    path('get_private_classes/',get_private_classes, name='get_private_classes'),
    path('add_new_session/',add_new_session, name='add_new_session'),

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
    path("delete_instructor/<int:instructor_id>/",delete_instructor,name="delete_instructor"),
    path("edit_instructor/<int:instructor_id>/",edit_instructor,name="edit_instructor"),
    path("studios/",get_studios,name="studios"),
    path("add_studio/",add_studio,name="add_studio"),
    path("delete_studio/<int:studio_id>/",delete_studio,name="delete_studio"),
    path("edit_studio/<int:studio_id>/",edit_studio,name="edit_studio"),
    path("packages/",get_packages,name="packages"),
    path('add_package/',add_package, name='add_package'),
    path('delete_package_type/<int:package_type_id>/',delete_package_type, name='delete_package_type'),
    path('delete_package/<int:package_id>/',delete_package, name='delete_package'),

]
