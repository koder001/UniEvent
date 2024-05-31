

from django.db import models
from studyroom.models import Room

class RecurringEvent(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ]

    WEEK_TYPE_CHOICES = [
        (0, 'Четная'),
        (1, 'Нечетная'),
        (2, 'Обе'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, 
        related_name='recurring_events', verbose_name="Аудитория", default=1)
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, 
        verbose_name="День недели", default=0)
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    week_type = models.IntegerField(choices=WEEK_TYPE_CHOICES, 
        verbose_name="Четность недели", default=2)

    class Meta:
        verbose_name = "расписание"
        verbose_name_plural = "Расписание"
    def __str__(self):
        return f"{self.get_weekday_display()} {self.start_time}-{self.end_time}"
