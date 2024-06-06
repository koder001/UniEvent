from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room

@login_required
def room_list(request):
    rooms = Room.objects.all().order_by('location', 'name')
    locations = {}
    for room in rooms:
        if room.location not in locations:
            locations[room.location] = []
        locations[room.location].append(room)
    
    context = {
        'locations': locations,
    }
    return render(request, 'studyroom/room_list.html', context)
