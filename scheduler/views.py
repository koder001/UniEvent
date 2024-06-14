from django.shortcuts import render, redirect
from .forms import RecurringEventForm
from .models import RecurringEvent, Room
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction

# Константы для периодов и дней недели
PERIODS = {
    '1': '9:00-10:30',
    '2': '10:40-12:10',
    '3': '13:00-14:30',
    '4': '14:40-16:10'
}
DAYS = range(7)  # Понедельник до Воскресенья

@staff_member_required
def create_recurring_event(request):
    """Создание расписания."""
    if request.method == 'POST':
        form = RecurringEventForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            week_type = form.cleaned_data['week_type']

            # Удаляем старые записи с такой же четностью или "обе"
            with transaction.atomic():
                if week_type == 0:
                    RecurringEvent.objects.filter(room=room, week_type__in=[0, 2]).delete()
                elif week_type == 1:
                    RecurringEvent.objects.filter(room=room, week_type__in=[1, 2]).delete()
                else:
                    RecurringEvent.objects.filter(room=room, week_type__in=[0, 1, 2]).delete()

                new_events = []
                for day in DAYS:
                    for period, times in PERIODS.items():
                        if f"{day}-{period}" in request.POST:
                            start_time, end_time = times.split('-')
                            new_events.append(RecurringEvent(
                                room=room,
                                weekday=day,
                                start_time=start_time,
                                end_time=end_time,
                                week_type=week_type
                            ))
                RecurringEvent.objects.bulk_create(new_events)

            return redirect('all_recurring_events')
    else:
        form = RecurringEventForm()

    rooms = Room.objects.all()
    return render(request, 'scheduler/create_recurring_event.html', {'form': form, 'rooms': rooms, 'periods': PERIODS, 'days': DAYS})

@staff_member_required
def all_recurring_events(request):
    """Отображение расписания."""
    events = RecurringEvent.objects.all().order_by('room', 'week_type', 'weekday', 'start_time')
    grouped_events = {}

    for event in events:
        room_week_key = (event.room, event.get_week_type_display())
        if room_week_key not in grouped_events:
            grouped_events[room_week_key] = []
        grouped_events[room_week_key].append(event)

    return render(request, 'scheduler/all_recurring_events.html', {
        'grouped_events': grouped_events,
        'periods': PERIODS,
        'days': DAYS,
    })
