from django import forms
from calendarapp.models import Event, EventMember
from calendarapp.models.event import Instructor, StudioLocation, Package, ClassOccurrence

class EventForm(forms.ModelForm):
    DAYS_OF_WEEK = [
        ("Sunday", "Sunday"),
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    ]

    days = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select the days for this class.",
    )

    class Meta:
        model = Event
        fields = ["name", "studio_location", "instructor", "days", "from_time", "to_time", "start_duration", "end_duration"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Class name"}),
            "studio_location": forms.Select(attrs={"class": "form-control"}),
            "instructor": forms.Select(attrs={"class": "form-control"}),
            "from_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "to_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "start_duration": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_duration": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class AddPrivateClass(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "instructor", "start_duration", "from_time", "to_time"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Class name"}),
            "instructor": forms.Select(attrs={"class": "form-control"}),
            "start_duration": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "from_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "to_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }
      
class AddOtherClass(forms.ModelForm):
    DAYS_OF_WEEK = [
        ("Sunday", "Sunday"),
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    ]

    days = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select the days for this event.",
    )

    class Meta:
        model = Event
        fields = ["name", "studio_location", "days", "start_duration", "end_duration", "from_time", "to_time"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Class name"}),
            "studio_location": forms.Select(attrs={"class": "form-control"}),
            "start_duration": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_duration": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "from_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "to_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }  
        
class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]

class AddInstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ["name","phone_number","share_percentage_group", "share_percentage_private"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Instructor Name"}
            ),
            "phone_number": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter 11-digit phone number", "type": "tel", "pattern": "[0-9]{11}", "maxlength": "11"}
            ),
            "share_percentage_group": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter group share percentage"}
            ),
            "share_percentage_private": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter private share percentage"}
            ),
        }
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit() or len(phone_number) != 11:
            raise forms.ValidationError("Phone number must be exactly 11 digits.")
        return phone_number

    def clean_share_percentage_group(self):
        share_percentage_group = self.cleaned_data.get("share_percentage_group")
        if share_percentage_group < 0 or share_percentage_group > 100:
            raise forms.ValidationError("Share percentage must be between 0 and 100.")
        return share_percentage_group
    
    def clean_share_percentage_private(self):
        share_percentage_private = self.cleaned_data.get("share_percentage_private")
        if share_percentage_private < 0 or share_percentage_private > 100:
            raise forms.ValidationError("Share percentage must be between 0 and 100.")
        return share_percentage_private
     
class AddStudioForm(forms.ModelForm):
    class Meta:
        model = StudioLocation
        fields = ["name","address","share_percentage"]
        
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['package_type', 'number_of_sessions', 'member_price', 'non_member_price','member_price_per_class', 'non_member_price_per_class', 'duration']
        widgets = {
            'package_type': forms.Select(attrs={'class': 'form-control'}),
            'number_of_sessions': forms.NumberInput(attrs={'class': 'form-control'}),
            'member_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'non_member_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'member_price_per_class': forms.NumberInput(attrs={'class': 'form-control'}),
            'non_member_price_per_class': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
class AddOccurrenceClassForm(forms.ModelForm):
    class Meta:
        model = ClassOccurrence
        fields = ["date", "from_time", "to_time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "from_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "to_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }
        