from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Group, Institution

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name='Test Institution', 
            fullname='Full Name of Test Institution')
        self.group = Group.objects.create(name='Test Group', 
            fullname='Full Name of Test Group', institution=self.institution)
        self.user = UserProfile.objects.create(email='test@example.com', 
            first_name='Test', last_name='User')

    def test_userprofile_creation(self):
        """Test UserProfile model creation."""
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.first().email, 'test@example.com')


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.institution = Institution.objects.create(name='Test Institution', fullname='Full Name of Test Institution')
        self.group = Group.objects.create(name='Test Group', fullname='Full Name of Test Group', institution=self.institution)
        # Создаем пользователя с правильным паролем
        self.user = UserProfile.objects.create_user(email='test@example.com', first_name='Test', last_name='User', password='testpassword')

    def test_user_login_view(self):
        """Test user login view."""
        response = self.client.post(reverse('login'), {'username': self.user.email, 'password': 'testpassword'})
        self.assertRedirects(response, reverse('dashboard'))  # Проверяем успешный редирект на страницу dashboard


    def test_user_dashboard_view(self):
        """Test user dashboard view."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/dashboard.html')

    def test_user_register_view(self):
        """Test user registration view."""
        response = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password2': 'newpassword',
            'group_student': self.group.pk
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register_done.html')
        self.assertEqual(UserProfile.objects.count(), 2)  # One user was created in setup

    def test_user_edit_profile_view(self):
        """Test user edit profile view."""
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'Edited',
            'last_name': 'User',
            'email': 'test@example.com',
            'group_student': self.group.pk
        })
        self.assertEqual(response.status_code, 302)  # Check redirection after successful profile edit
        self.assertTrue(response.url.startswith('/user/dashboard/'))
