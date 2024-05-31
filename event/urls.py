from django.urls import path
from . import views
urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('event/archive/', views.event_archive, name='event_archive'),
    path('room_filter/', views.room_filter, name='room_filter'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/unsubscribe/', views.event_unsubscribe, name='event_unsubscribe'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
]
