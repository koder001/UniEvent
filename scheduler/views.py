from django.shortcuts import render, redirect
from .forms import RecurringEventForm
from .models import RecurringEvent, Room
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def create_recurring_event(request):
    periods = {
        '1': '9:00-10:30',
        '2': '10:40-12:10',
        '3': '13:00-14:30',
        '4': '14:40-16:10'
    }
    days = range(7)  # Понедельник до Воскресенья

    if request.method == 'POST':
        form = RecurringEventForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            week_type = form.cleaned_data['week_type']
            print(week_type)

            # Удаляем старые записи с такой же четностью или "обе"
            if week_type == 0:
                RecurringEvent.objects.filter(room=room, week_type__in=[0, 2]).delete()
            elif week_type == 1:
                RecurringEvent.objects.filter(room=room, week_type__in=[1, 2]).delete()
            else:
                RecurringEvent.objects.filter(room=room, week_type__in=[0, 1, 2]).delete()

            for day in days:
                for period, times in periods.items():
                    if f"{day}-{period}" in request.POST:
                        start_time, end_time = times.split('-')
                        RecurringEvent.objects.create(
                            room=room,
                            weekday=day,
                            start_time=start_time,
                            end_time=end_time,
                            week_type=week_type
                        )
            messages.success(request, 'Циклическое мероприятие успешно создано!')
            return redirect('create_recurring_event')  # Перенаправление на ту же страницу
    else:
        form = RecurringEventForm()

    rooms = Room.objects.all()
    return render(request, 'scheduler/create_recurring_event.html', {'form': form, 'rooms': rooms, 'periods': periods, 'days': days})

