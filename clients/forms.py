from django import forms
from .models import Client, Registration
from calendarapp.models.event import Package


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'phone_number',
            'email',
            'address',
            'preferred_time',
            'is_member',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'preferred_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred time'}),
            'is_member': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RegistrationStep1Form(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['client', 'class_obj', 'package_type', 'package', 'payment_type', 'payment_method']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'class_obj': forms.Select(attrs={'class': 'form-control'}),
            'package_type': forms.Select(attrs={'class': 'form-control'}),
            'package': forms.Select(attrs={'class': 'form-control'}),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['package'].queryset = Package.objects.none()

        if 'package_type' in self.data:
            try:
                package_type_id = int(self.data.get('package_type'))
                self.fields['package'].queryset = Package.objects.filter(package_type_id=package_type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['package'].queryset = self.instance.package_type.package_set.all()

class RegistrationStep2Form(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['price_paid']
        widgets = {
            'price_paid': forms.NumberInput(attrs={'class': 'form-control'}),
        }
