from django.contrib import admin
from .models import Room, Location

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'description', 'location', 'photo')  

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)  
