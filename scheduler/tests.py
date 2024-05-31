from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import RecurringEvent, Room
from studyroom.models import Location
from .forms import RecurringEventForm
from user.models import UserProfile


User = get_user_model()

class RecurringEventTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Main Building")
        self.room = Room.objects.create(name="Room 101", capacity=10, location=self.location)
        self.recurring_event = RecurringEvent.objects.create(
            room=self.room,
            weekday=0,
            start_time='09:00:00',
            end_time='10:30:00',
            week_type=2
        )

    def test_recurring_event_creation(self):
        self.assertEqual(self.recurring_event.room, self.room)
        self.assertEqual(self.recurring_event.weekday, 0)
        self.assertEqual(str(self.recurring_event), "Понедельник 09:00:00-10:30:00")

class RecurringEventFormTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Main Building")
        # Создаем аудиторию для местоположения
        self.room = Room.objects.create(name="Room 101", capacity=10, location=self.location)

    def test_recurring_event_form_valid(self):
        # Используем созданную аудиторию для формы
        form_data = {
            'room': self.room.id,
            'week_type': 2,
        }
        form = RecurringEventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recurring_event_form_invalid(self):
        form_data = {
            'room': '',
            'week_type': 2,
        }
        form = RecurringEventForm(data=form_data)
        self.assertFalse(form.is_valid())
        
class CreateRecurringEventViewTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(email='test@example.com', password='password')
        self.client.login(email='test@example.com', password='password')

    def test_create_recurring_event_view(self):
        response = self.client.get(reverse('create_recurring_event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduler/create_recurring_event.html')
