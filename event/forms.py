from django import forms
from .models import Event, EventRegistration
from studyroom.models import Location
from user.models import UserProfile 

class EventForm(forms.ModelForm):
    organizer = forms.ModelChoiceField(
        label='Организатор', 
        queryset=UserProfile.objects.all(),
        widget=forms.Select(attrs={'style': 'max-width: 30ch;'})
    )


    location = forms.ModelChoiceField(
        label='Расположение', 
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'style': 'max-width: 40ch;'})
    )

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
