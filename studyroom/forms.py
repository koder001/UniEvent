from django import forms
from .models import Room, Location

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'capacity', 'photo', 'location']
