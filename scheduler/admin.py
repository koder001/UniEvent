from django.contrib import admin
from .models import RecurringEvent

@admin.register(RecurringEvent)
class RecurringEventAdmin(admin.ModelAdmin):
    list_display = ('room', 'week_type', 'weekday', 'start_time', 'end_time')
    list_filter = ('weekday', 'week_type', 'room')
    ordering = ('weekday', 'start_time')
