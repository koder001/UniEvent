from django.test import TestCase, Client
from django.urls import reverse
from .models import Room, Location
from .forms import RoomForm
from user.models import UserProfile

class LocationModelTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Main Building")

    def test_location_creation(self):
        self.assertEqual(self.location.name, "Main Building")
        self.assertEqual(str(self.location), "Main Building")

class RoomModelTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Main Building")
        self.room = Room.objects.create(
            name="Room 101",
            description="A small conference room.",
            capacity=10,
            location=self.location
        )

    def test_room_creation(self):
        self.assertEqual(self.room.name, "Room 101")
        self.assertEqual(self.room.description, "A small conference room.")
        self.assertEqual(self.room.capacity, 10)
        self.assertEqual(self.room.location, self.location)
        self.assertEqual(str(self.room), "Room 101")

class RoomFormTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Main Building")

    def test_room_form_valid(self):
        form_data = {
            'name': 'Room 101',
            'description': 'A small conference room.',
            'capacity': 10,
            'location': self.location.id
        }
        form = RoomForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_room_form_invalid(self):
        form_data = {
            'name': '',
            'description': 'A small conference room.',
            'capacity': 10,
            'location': self.location.id
        }
        form = RoomForm(data=form_data)
        self.assertFalse(form.is_valid())

class RoomListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(email='testuser@example.com', password='password')
        self.location = Location.objects.create(name="Main Building")
        self.room1 = Room.objects.create(name="Room 101", capacity=10, location=self.location)
        self.room2 = Room.objects.create(name="Room 102", capacity=20, location=self.location)

    def test_room_list_view_with_login(self):
        self.client.login(email='testuser@example.com', password='password')
        response = self.client.get(reverse('room_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studyroom/room_list.html')
        self.assertContains(response, 'Room 101')
        self.assertContains(response, 'Room 102')
