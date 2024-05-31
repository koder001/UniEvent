from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'organizer', 'location', 'get_rooms', 'start_time', 'end_time', 'image')
	list_filter = ('start_time', 'end_time')

	def get_rooms(self, obj):
		return ", ".join([room.name for room in obj.rooms.all()])
	get_rooms.short_description = 'Аудитории'

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
	list_display = ('user', 'event', 'registered_at')
	list_filter = ('registered_at', 'event')

