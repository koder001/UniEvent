from django import forms
from .models import RecurringEvent

class RecurringEventForm(forms.ModelForm):
    class Meta:
        model = RecurringEvent
        fields = ['room', 'week_type']
