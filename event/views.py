from django.shortcuts import render, redirect
from .models import Room, Event, Location, EventRegistration
from scheduler.models import RecurringEvent
from .forms import EventForm, EventRegistrationForm
from django.http import JsonResponse
from django.core import serializers
from django.db import models
import datetime
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

@staff_member_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Создаем экземпляр Event, но пока не сохраняем его
            event = form.save(commit=False)
            # Сохраняем фото

            event.image = request.FILES.get('image')
            # Сохраняем объект Event в базу данных
            event.save()

            # Получаем список выбранных аудиторий из запроса (если таковые имеются)
            selected_rooms = request.POST.getlist('rooms')

            # Добавляем выбранные аудитории к объекту Event
            for room_id in selected_rooms:
                room = Room.objects.get(id=room_id)
                event.rooms.add(room)

            # Сохраняем объект Event с добавленными аудиториями
            event.save()

            return redirect('event_detail', event_id=event.id)  # Перенаправление на страницу с деталями мероприятия
    else:
        form = EventForm()

    # Передача пустого списка аудиторий в шаблон при первой загрузке страницы
    rooms = []  
    return render(request, 'event/create_event.html', {'form': form, 'rooms': rooms})


def room_filter(request):
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    location_id = request.POST.get('location')

    rooms = Room.objects.all()

    if start_time and end_time and start_time < end_time and location_id:
        rooms = rooms.exclude(events__start_time__lt=end_time, events__end_time__gt=start_time)
        rooms = rooms.filter(location_id=int(location_id))

        # Преобразуем дату начала мероприятия в день недели (0 - Понедельник, 1 - Вторник, ..., 6 - Воскресенье)
        start_date = request.POST.get('start_time').split("T")[0]

        start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        start_weekday = start_date_obj.weekday()

        # Определяем четность недели с начала года
        year_start = datetime.datetime(start_date_obj.year, 1, 1)
        week_number = (start_date_obj - year_start).days // 7 + 1
        if week_number % 2 == 0:
            week_type = 0
        else:
            week_type = 1
        
        # Разделяем время начала и окончания на часы и минуты
        start_time = request.POST.get('start_time').split("T")[1]
        end_time = request.POST.get('end_time').split("T")[1]

        # Ищем совпадения в расписании
        conflicting_rooms = RecurringEvent.objects.filter(
            weekday=start_weekday
        ).filter(
            models.Q(start_time__lt=end_time, end_time__gt=start_time) &
            (models.Q(week_type=week_type) | models.Q(week_type=2))
        ).values_list('room', flat=True)

        rooms = rooms.exclude(id__in=conflicting_rooms)

    else:
        rooms = []

    rooms_json = serializers.serialize('json', rooms)
    return JsonResponse({'rooms': rooms_json})
    
@staff_member_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            if 'image' in request.FILES:
                event.image = request.FILES['image']
            event.save()

            selected_rooms = request.POST.getlist('rooms')
            event.rooms.clear()
            for room_id in selected_rooms:
                room = Room.objects.get(id=room_id)
                event.rooms.add(room)
            event.save()

            return redirect('event_detail', event_id=event.id)
    else:
        event.start_time = event.start_time.strftime('%Y-%m-%dT%H:%M')
        event.end_time = event.end_time.strftime('%Y-%m-%dT%H:%M')
        form = EventForm(instance=event)       
        rooms = event.rooms.all()
    
    return render(request, 'event/edit_event.html', {'form': form, 'event': event, 'rooms': rooms})
    
def event_list(request):
    upcoming_events = Event.objects.filter(end_time__gte=timezone.now()).order_by('start_time')
    return render(request, 'event/event_list.html', {'events': upcoming_events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_event_passed = event.end_time < timezone.now()
    
    if request.method == 'POST':
        if not is_event_passed:
            form = EventRegistrationForm(request.POST)
            if form.is_valid():
                registration, created = EventRegistration.objects.get_or_create(user=request.user, event=event)
                if created:
                    return redirect('event_detail', event_id=event.id)
    else:
        form = EventRegistrationForm()
    
    is_registered = EventRegistration.objects.filter(user=request.user, event=event).exists()
    return render(request, 'event/event_detail.html', {
        'event': event,
        'form': form,
        'is_registered': is_registered,
        'is_event_passed': is_event_passed,
    })

def archive_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_event_passed = event.end_time < timezone.now()
    is_registered = EventRegistration.objects.filter(user=request.user, event=event).exists()
    
    return render(request, 'event/archive_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'is_event_passed': is_event_passed,
    })

def event_unsubscribe(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registration = EventRegistration.objects.filter(user=request.user, event=event)
    if registration.exists():
        registration.delete()
    return redirect('event_detail', event_id=event_id)


def event_archive(request):
    past_events = Event.objects.filter(end_time__lt=timezone.now()).order_by('-start_time')
    return render(request, 'event/event_archive.html', {'events': past_events})