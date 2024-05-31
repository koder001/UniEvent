from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название расположения")

    def __str__(self):
        return self.name  

    class Meta:
        verbose_name = "расположение"
        verbose_name_plural = "Расположения"

class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название аудитории")
    description = models.TextField(verbose_name="Описание", blank=True)
    capacity = models.IntegerField(verbose_name="Вместимость")
    photo = models.ImageField(upload_to='room_photos/', verbose_name="Фотография", 
    	blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, 
    	related_name='rooms', verbose_name="Расположение", default=0)

    class Meta:
        verbose_name = "помещение"
        verbose_name_plural = "Помещения"

    def __str__(self):
        return self.name
