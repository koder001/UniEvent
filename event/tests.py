from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Event
from .forms import EventForm
from studyroom.models import Location, Room

User = get_user_model()

class EventTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Main Building")
        self.room = Room.objects.create(name="Room 101", capacity=10, location=self.location)
        self.user = User.objects.create(email='test@example.com', password='password')
        self.event = Event.objects.create(
            organizer=self.user,
            location=self.location,
            name="Test Event",
            description="Test Description",
            start_time='2024-05-25 10:00:00',
            end_time='2024-05-25 12:00:00',
            image=None
        )

    def test_event_creation(self):
        self.assertEqual(self.event.organizer, self.user)
        self.assertEqual(self.event.location, self.location)
        self.assertEqual(self.event.name, "Test Event")
        self.assertEqual(self.event.description, "Test Description")
        self.assertEqual(str(self.event.start_time), '2024-05-25 10:00:00')
        self.assertEqual(str(self.event.end_time), '2024-05-25 12:00:00')

class EventFormTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Main Building")
        self.user = User.objects.create(email='test@example.com', password='password')
        self.room = Room.objects.create(name="Room 101", capacity=10, location=self.location)

    def test_event_form_valid(self):
        form_data = {
            'organizer': self.user.id,
            'location': self.location.id,
            'name': 'Test Event',
            'description': 'Test Description',
            'start_time': '2024-05-25T10:00',
            'end_time': '2024-05-25T12:00',
            'rooms': [self.room.id],
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_form_invalid(self):
        form_data = {
            'organizer': self.user.id,
            'location': self.location.id,
            'name': '',
            'description': 'Test Description',
            'start_time': '2024-05-25T10:00',
            'end_time': '2024-05-25T12:00',
            'rooms': [self.room.id],
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

class CreateEventViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', password='password')
        self.client.login(email='test@example.com', password='password')

    def test_create_event_view(self):
        response = self.client.get(reverse('create_event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/create_event.html')

# Здесь можно добавить тесты для остальных представлений и функций вашего приложения
