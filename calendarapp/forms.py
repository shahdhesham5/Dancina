from django import forms
from django.forms import ModelForm, DateInput
from calendarapp.models import Event, EventMember
from calendarapp.models.event import Instructor, StudioLocation, Package

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


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
        fields = ["name","address"]
        
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['package_type', 'number_of_sessions', 'member_price', 'non_member_price']
        widgets = {
            'package_type': forms.Select(attrs={'class': 'form-control'}),
            'number_of_sessions': forms.NumberInput(attrs={'class': 'form-control'}),
            'member_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'non_member_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }