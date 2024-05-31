from django.db import models
from studyroom.models import Room, Location
from user.models import UserProfile

class Event(models.Model):
    organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, 
        related_name='organized_events', verbose_name="Организатор")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, 
        related_name='events', verbose_name="Расположение")
    rooms = models.ManyToManyField(Room, related_name='events', 
        verbose_name="Аудитории")
    name = models.CharField(max_length=255, verbose_name="Название мероприятия")
    description = models.TextField(verbose_name="Описание")
    start_time = models.DateTimeField(verbose_name="Дата и время начала")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания")
    image = models.ImageField(upload_to='event_images/', 
        blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.name

class EventRegistration(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='registrations', verbose_name="Пользователь")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations', verbose_name="Мероприятие")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "регистрация на мероприятие"
        verbose_name_plural = "Регистрации на мероприятия"
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.email} - {self.event.name}"

