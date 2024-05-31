from django import forms
from .models import Event
from .models import EventRegistration

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['organizer', 'name', 'description', 'image', 'start_time', 'end_time', 'location']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        } 

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = []
