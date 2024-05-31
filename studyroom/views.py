from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room

@login_required
def room_list(request):
    """Представление для отображения списка доступных аудиторий."""
    rooms = Room.objects.all()
    return render(request, 'studyroom/room_list.html', {'rooms': rooms})


