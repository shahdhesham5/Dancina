from django.contrib import admin
from calendarapp.models.event import StudioLocation, Instructor, PackageType, Package, Event, ClassOccurrence
from calendarapp.models.event_member import EventMember

@admin.register(StudioLocation)
class StudioLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address','share_percentage')
    search_fields = ('name',)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'share_percentage_group','share_percentage_private')
    search_fields = ('name', 'phone_number')

@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    model = PackageType
    list_display = ('name',)
    
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    model = Package
    list_display = ('number_of_sessions', 'member_price', 'non_member_price')
    

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ["id", "name", "studio_location", "instructor", "user", "days", "from_time", "to_time","start_duration","end_duration", "is_private","is_active", "is_deleted"]
    list_filter = ["is_active", "is_deleted", "days"]
    search_fields = ["name"]

@admin.register(ClassOccurrence)
class ClassOccurrenceAdmin(admin.ModelAdmin):
    model = ClassOccurrence
    list_display = ["id", "event", "date"]


@admin.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    model = EventMember
    list_display = ["id", "event", "user", "created_at", "updated_at"]
    list_filter = ["event"]
